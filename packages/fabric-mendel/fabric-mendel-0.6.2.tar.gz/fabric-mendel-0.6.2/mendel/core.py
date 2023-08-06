from datetime import datetime
from functools import partial
import getpass
import json
import os
import sys
import urllib2

import requests
from debian import deb822

from fabric.colors import red, green, magenta, blue, yellow
from fabric.context_managers import cd, lcd, hide
from fabric.contrib import files
from fabric.operations import sudo, local, run, prompt, put
from fabric.state import env
from fabric.tasks import WrappedCallableTask

from mendel.conf import Config
from mendel.util import lcd_task

config = Config()

if getattr(env, '_already_built', None) is None:
    env._already_built = False

###############################################################################
# TODO - add example services in python, demonstrate crons can
# also work
# TODO - add vagrant box with examples
# TODO drop a file into release directories that are "successful"
# TODO so we don't roll back to a failed build. either that or we cleanup after
# TODO ourselves



# TODO remote_deb will replace deb as soon as we can get all those services
# TODO using `deb` migrated into nexus. For now we need to support both though
###############################################################################

class Mendel(object):
    """
    A class for managing service deployments


    TODO document every field


    Instantiate a Mendel instance in your fabfile,
    and then delegate to it to perform tasks.

        #fabfile.py

        from mendel import Mendel

        mendel = Mendel(service_name='my-service')

        @task
        def deploy():
            mendel.deploy()

        @task
        def upload():
            mendel.upload()


    Fabric will also automatically discover any
    Task instances in your fabfile, so you can use
    get_tasks to instantiate all of them

        from mendel import Mendel

        d = Mendel(
                service_name='sproutqueue-global',
                build_target_path='target',
                user='sq-global',
                bundle_type='deb'
        )

        upload, deploy, install, build, tail, rollback, upstart, link_latest_release = d.get_tasks()

    and then you can

        fab upload
    or
        fab deploy
    or
        fab tail

    etc etc etc



    """
    def __init__(
            self,
            service_name,
            service_root=None,
            build_target_path=None,
            user=None,
            group=None,
            bundle_type=None,
            project_type=None,
            cwd=None,
            jar_name=None,
            nexus_user=None,
            nexus_host=None,
            nexus_port=None,
            nexus_repository=None,
            graphite_host=None,
            **kwargs
    ):

        self._service_name = service_name
        self._service_root = service_root or os.path.join('/srv', self._service_name)
        self._build_target_path = build_target_path or 'target/%s' % self._service_name
        self._user = user or service_name
        self._group = group or user or service_name
        self._bundle_type = bundle_type or 'jar'
        self._project_type = project_type or 'java'
        self._cwd = cwd or '.'
        self._jar_name = jar_name or service_name

        self._version_control = "hg" if os.path.exists(".hg") else "git"
        self._release_dir = None

        self._nexus_user = nexus_user or config.NEXUS_USER
        self._nexus_host = nexus_host or config.NEXUS_HOST
        self._nexus_port = nexus_port or config.NEXUS_PORT
        self._nexus_repository = nexus_repository or config.NEXUS_REPOSITORY

        self._graphite_host = graphite_host or config.GRAPHITE_HOST

        # Hack -- Who needs polymorphism anyways?
        #
        # but really, TODO make subclasses for each bundle type
        # when this supports python AND java,
        # will probably want a builder delegate and a deployer delegate
        # because cross products
        if bundle_type == 'tgz':
            self._install = self._install_tgz
            self._upload = self._upload_tgz
            self._rollback = self._symlink_rollback
        elif bundle_type == 'deb':
            self._install = self._install_deb
            self._upload = self._upload_deb
            self._rollback = self._symlink_rollback
        elif bundle_type == 'jar':
            self._install = self._install_jar
            self._upload = self._upload_jar
            self._rollback = self._symlink_rollback
        elif bundle_type == 'remote_deb':
            self._install = self._install_remote_deb
            self._upload = self._upload_remote_deb
            self._rollback = self._apt_rollback

            # this is a hack, we "build" during
            # the "upload" task via `mvn deploy`
            self._mark_as_built()

    def __call__(self, task_name, *args, **kwargs):
        task = getattr(self, task_name, None)
        if task:
            task(*args, **kwargs)
        else:
            import inspect
            tasks = inspect.getmembers(self, predicate=inspect.ismethod)
            print red("Invalid task name: %s"% task_name)
            print
            print "Please choose one of" 
            print 
            for task, _ in tasks:
                if not task.startswith("_"):
                    print "\t" + task

    ############################################################################
    # Helper methods
    ############################################################################

    def _lpath(self, *args):
        return os.path.join(self._cwd, *args)

    def _rpath(self, *args):
        return os.path.join(self._service_root, *args)

    def _tpath(self, *args):
        return os.path.join('/tmp', *args)

    def _create_if_missing(self, path):
        if not files.exists(path):
            sudo('mkdir -p %s' % path, user=self._user, group=self._group)

    def _change_symlink_to(self, release_path):
        print blue("Linking release %s into current" % release_path)
        with cd(self._rpath()):
            sudo('ln -sfT %s current' % release_path, user=self._user, group=self._group)

    def _get_commit_hash(self):
        """
        Obtain commit hash that the repository is currently at, so we can tag the release dir with it as well
        as report the commit hash of what's deployed. Note that this is not the "latest" commit intentionally, it is the
        commit hash that the repository is currently pointed to.

        Note: Does not support git repositories yet.
        """
        if self._version_control is "hg":
            commithash = local('hg id -i', capture=True)
        elif self._version_control is "git":
            commithash = local('git rev-parse HEAD', capture=True)
        else:
            raise Exception("Unsupported version control: %s", self._version_control)

        if commithash.failed or commithash.strip() == '':
            print red("failed to obtain commit hash. are you in a mercurial repo? i don't support git yet, sorry, issue a PR")
            sys.exit(1)
        return commithash.strip()

    def _new_release_dir(self):
        """
        generate a new release dir for the remote hosts, this needs to be the same across hosts
        to make it clearer that they all have the same release/build. yes this is semi-brittle,
        but for most situations it should be adequate. introducing amazon S3 to hold builds
        could make this less brittle. having CI would be even better but we're not there yet.
        """
        if self._release_dir is None:
            release_dir_args = (datetime.utcnow().strftime('%Y%m%d-%H%M%S'), getpass.getuser(), self._get_commit_hash())
            self._release_dir = '%s-%s-%s' % release_dir_args
        return self._release_dir

    def _mark_as_built(self):
        """
        so we dont build multiple times for each host we're deploying too.
        that's silly :)
        """
        env._already_built = True

    def _is_already_built(self):
        return env._already_built

    def _get_bundle_name(self):
        try:
            with lcd(self._lpath(self._build_target_path)):
                if self._bundle_type == "tgz":
                    r = local('ls *.tar.gz', capture=True)
                elif self._bundle_type == "deb":
                    r = local('ls *.deb', capture=True)
                elif self._bundle_type == "jar":
                    r = local('ls %s.jar' % self._jar_name, capture=True)
                elif self._bundle_type == "remote_deb":
                    return None
                else:
                    raise Exception('Unsupported bundle type: %s' % self._bundle_type)
        except:
            print 'could not find bundle in build_target_path:', self._lpath(self._build_target_path)
            raise
        if r.failed:
            raise Exception('couldn\'t find bundle in %s' % self._lpath(self._build_target_path))
        bundle_file = r.strip()
        return bundle_file

    def _get_current_release(self):
        with cd(self._rpath()):
            y = sudo('readlink current', user=self._user, group=self._group)
            current_release = y.split('/')[-1].strip()
        return current_release

    def _get_all_releases(self):
        x = sudo('ls -1 %s' % self._rpath('releases'), user=self._user, group=self._group)
        releases = sorted([_.strip() for _ in x.split('\n') if _.strip() != ''])
        return releases

    def _display_releases_for_rollback_selection(self, releases, current):
        """
        displays releases with current release flagged, also returns index of
        current release in release list
        """
        r_list, curr_index = [], None
        for i, r in enumerate(releases):
            if r == current:
                r_list.append(r + ' <-- current')
                curr_index = i
            else:
                r_list.append(r)

        for r in r_list:
            print(r)

        return curr_index

    def _display_apt_versions_for_rollback_selection(self, releases, current):
        """
        displays releases with current release flagged, also returns index of
        current release in release list
        """
        r_list, curr_index = [], None
        for i, r in enumerate(releases):
            release_string = ('%s %s' % (r.get('Version'), r.get('Filename', '').split('/')[-1]))
            if current == r.get('Version'):
                r_list.append(release_string + green(' <-- current'))
                curr_index = i
            else:
                r_list.append(release_string)

        for r in r_list:
            print(r)

        return curr_index

    def _is_running(self):
        result = self.upstart('status', print_output=False)
        return 'start/running' in result

    def _start_or_restart(self):
        if self._is_running():
            self.upstart('restart')
        else:
            self.upstart('start')

    def _missing_hosts(self):
        return not bool(env.hosts)

    def _get_latest_release(self):
        with hide('stdout', 'running'):
            return run('ls -lt %s' % self._rpath('releases')).split('\n')[1].split()[-1]

    def _dpkg_install_deb(self, fq_bundle_file):
        with hide('stdout'):
            sudo('dpkg --force-confold -i %s' % fq_bundle_file)

    def _apt_install_remote_deb_latest(self):
        print blue('upgrading package %s to latest available version' % self._service_name)
        with hide('stdout'):
            sudo('apt-get update')
        sudo(
            'apt-get install '
            '-y '
            '--force-yes '
            '--only-upgrade '
            '-o Dpkg::Options::="--force-confold" '
            '%s'  % self._service_name
        )

    def _apt_install_remote_deb(self, version=None):
        if not version:
            self._apt_install_remote_deb_latest()

        else:
            print blue('installing %s %s ' % (self._service_name, version))
            with hide('stdout'):
                sudo('apt-get update')
            sudo(
                'apt-get install '
                '-y '
                '--force-yes '
                '-o Dpkg::Options::="--force-confold" '
                '%s=%s'  % (self._service_name, version)
            )

        jar_name = run('readlink %s.jar' % self._rpath("current", self._service_name))
        print green('apt installed new jar: %s' % jar_name)

    def _install_tgz(self, bundle_file):
        release_dir = self._new_release_dir()

        with cd(self._rpath('releases', release_dir)):
            # so we can delete it after extraction
            sudo('chown %s:%s %s' % (self._user, self._group, bundle_file))
            sudo('tar --strip-components 1 -zxvf %(bf)s && rm %(bf)s' % {'bf': bundle_file}, user=self._user, group=self._group)
            sudo('ln -sf *.jar %s.jar' % self._service_name, user=self._user, group=self._group)
            self._change_symlink_to(self._rpath('releases', release_dir))

    def _install_jar(self, jar_name):
        release_dir = self._new_release_dir()

        with cd(self._rpath('releases', release_dir)):
            sudo('chown %s:%s %s' % (self._user, self._group, jar_name))
            self._change_symlink_to(self._rpath('releases', release_dir))

    def _backup_current_release(self):
        """

        [advanced]\t

        dpkg likes to blow away your old files when 
        you make new ones. this is a hack to keep them 
        around
        """
        current_release = self._rpath('releases', self._get_current_release()).rstrip('/')

        should_backup = \
                '.old' not in current_release and \
                not files.exists(current_release + '.old')

        if should_backup:
            sudo('mv %(dir)s %(dir)s.old' % {'dir': current_release}, user=self._user, group=self._group)
            self._change_symlink_to("%s.old" % current_release)

    def _install_deb(self, bundle_file):
        self._backup_current_release()
        self._dpkg_install_deb(self._tpath(bundle_file))
        self.link_latest_release()

    def _install_remote_deb(self, *ignored):
        self._apt_install_remote_deb_latest()

    def _upload_tgz(self, bundle_file):
        """
        create a new release dir and upload tarball
        """
        self._create_if_missing(self._rpath('releases'))
        release_dir = self._new_release_dir()
        self._create_if_missing(self._rpath('releases', release_dir))
        fq_bundle_file = self._lpath(self._build_target_path, bundle_file)
        put(fq_bundle_file, self._rpath('releases', release_dir), use_sudo=True)

        return release_dir

    def _upload_deb(self, bundle_file):
        """
        upload a deb to /tmp,  return path
        """
        dest = self._tpath()
        fq_bundle_file = self._lpath(self._build_target_path, bundle_file)
        put(fq_bundle_file, dest)

        return dest

    def _upload_remote_deb(self, *ignored):
        """
        upload a deb to /tmp,  return path
        """
        if self._project_type == "java":
            local('mvn clean -U deploy')
        else:
            raise Exception("Unsupported project type: %s" % self._project_type)

    def _upload_jar(self, jar_name):
        """
        create a new release dir and upload tarball
        """
        self._create_if_missing(self._rpath('releases'))
        release_dir = self._new_release_dir()
        self._create_if_missing(self._rpath('releases', release_dir))
        fq_jar_name = self._lpath(self._build_target_path, jar_name)
        put(fq_jar_name, self._rpath('releases', release_dir), use_sudo=True)

        return release_dir

    def _symlink_rollback(self):
        def validator(rollback_candidate, release_list):
            if rollback_candidate == self._get_current_release():
                raise Exception(
                    'can\'t rollback to same version that is already deployed')

            if rollback_candidate not in release_list:
                raise Exception(
                    'invalid rollback selection: %s' % rollback_candidate)

            return rollback_candidate

        with hide('status', 'running', 'stdout'):
            all_releases = self._get_all_releases()
            if len(all_releases) <= 1:
                print red('Only 1 release available, nothing to rollback to :(')
                sys.exit(1)

            curr_index = self._display_releases_for_rollback_selection(
                all_releases,
                self._get_current_release()
            )

            default_rollback_choice = all_releases[max(curr_index - 1, 0)]
            is_valid = partial(validator, release_list=all_releases)
            rollback_to = prompt('Rollback to:',
                                 default=default_rollback_choice,
                                 validate=is_valid)
            with cd(self._rpath('releases', rollback_to)):
                self._change_symlink_to(self._rpath('releases', rollback_to))
                self._start_or_restart()
                print green('successfully rolled back %s to %s' % (
                    self._service_name, rollback_to))
        self._track_event('rolledback')

    def _get_available_nexus_versions(self):
        # validate nexus settings are configured first
        for suffix in ('host', 'port', 'user', 'repository'):
            if not getattr(self, '_nexus_%s' % suffix):
                print red('~/.mendel.conf is missing %s in [nexus] configuration section' % suffix)
                sys.exit(1)

        url_for_debug = (
                'http://%(nexus_host)s:%(nexus_port)s'
                '/nexus/content/repositories'
                '/%(nexus_repository)s'
                '/Packages' % dict(
            nexus_host=self._nexus_host,
            nexus_port=self._nexus_port,
            nexus_repository=self._nexus_repository
        ))

        print blue('Downloading packages from %s' % url_for_debug)

        #TODO maybe read password from maven settings?
        nexus_password = os.environ.get('MENDEL_NEXUS_PASSWORD') or \
                         getpass.getpass(prompt='Enter nexus password: ')

        packages_file = requests.get(
            'http://%(nexus_user)s:%(nexus_password)s'
            '@%(nexus_host)s:%(nexus_port)s'
            '/nexus/content/repositories'
            '/%(nexus_repository)s'
            '/Packages' % dict(
                nexus_user=self._nexus_user,
                nexus_password=nexus_password,
                nexus_host=self._nexus_host,
                nexus_port=self._nexus_port,
                nexus_repository=self._nexus_repository
            )
        ).content

        package_entries = [
            deb822.Packages(package_info)
            for package_info in packages_file.split('\n\n')
            if package_info
        ]

        available_versions = [
            p for p in package_entries
            if p.get('Package') == self._service_name
        ]

        print blue('Found %s available versions of %s' % (len(package_entries), self._service_name))

        return available_versions

    def _get_current_package_version(self):
        with hide('stdout'):
            package_info = run('dpkg-query -s %s' % self._service_name)
            pkg = deb822.Packages(package_info)
            return pkg.get('Version')

    def _apt_rollback(self):
        def validator(rollback_candidate):
            if rollback_candidate not in [v.get('Version') for v in available_versions]:
                raise Exception('invalid rollback selection: %s' % rollback_candidate)
            return rollback_candidate

        with hide('status', 'running', 'stdout'):
            available_versions = self._get_available_nexus_versions()
            current_version = self._get_current_package_version()

            curr_index = self._display_apt_versions_for_rollback_selection(
                available_versions,
                current_version
            )

            default_rollback_choice = available_versions[max(curr_index - 1, 0)]
            rollback_to = prompt(
                'Rollback to:',
                default=default_rollback_choice.get('Version'),
                validate=validator
            )
            self._apt_install_remote_deb(version=rollback_to)
        self._track_event('rolledback')

    ############################################################################
    # Deploy Tasks
    ############################################################################

    def build(self):
        """
        [advanced]\tbuilds new application bundle for your service using maven
        expects the output to be a .tar.gz application bundle containing all
        required files for a service. it is highly recommended that you use the
        maven-assembly-plugin as a standard, it makes bundling files together into
        archives straightforward.

        Note: only builds once, no matter how many hosts!
        """
        if not self._is_already_built():
            if self._project_type == "java":
                local('mvn clean -U package')
            else:
                raise Exception("Unsupported project type: %s" % self._project_type)
            self._mark_as_built()

    def link_latest_release(self):
        """
        [advanced]\tcowboy it -- Links the most recent release into current
        """
        with hide('status', 'running', 'stdout'):
            release_dir = self._get_latest_release()
        print green("Linking release %s into current" % magenta(release_dir))
        self._change_symlink_to(self._rpath('releases', release_dir))

    def upload(self):
        """
        [advanced]\tupload your bundle to the server
        """
        try:
            bundle_file = self._get_bundle_name()
        except Exception as e:
            print red(e.message)
            sys.exit(1)

        dest = self._upload(bundle_file)
        if bundle_file:
            print green('Uploaded new release of %s to %s' % (bundle_file, dest))

    def install(self):
        """
        [advanced]\tinstall latest build on the hosts you specify
        """
        try:
            bundle_file = self._get_bundle_name()
        except Exception as e:
            print red(e.message)
            sys.exit(1)

        self._install(bundle_file)
        print green('Successfully installed new release of %s service' % self._service_name)

    def deploy(self):
        """
        [core]\t\tbuilds, installs, and deploys to all the specified hosts
        """
        if self._missing_hosts():
            print red("error: you didnt specify any hosts with -H")
            sys.exit(1)
        self.build()
        self.upload()
        self.install()
        self._start_or_restart()
        self._track_event('deployed')

    def rollback(self):
        """
        [core]\t\tchoose a version to rollback to from all available releases
        """
        self._rollback()

    def upstart(self, cmd, print_output=True):
        """
        [advanced]\t'start', 'stop', 'restart', or get the 'status' of your service
        """
        allowed = ('start', 'stop', 'restart', 'status')
        if cmd not in allowed:
            print red('unknown command, try one of %s' % ','.join(allowed))
            return
        with hide('status', 'running', 'stdout'):
            if print_output:
                print blue('executing upstart:%s' % cmd)
            out = sudo('%s %s' % (cmd, self._service_name))
            if print_output:
                print green(out)
            return out

    def tail(self, log_name="output.log"):
        """
        [core]\t\twatch the logs
        """
        if len(env.hosts) > 1:
            print red("can only tail logs on one host at a time")
            sys.exit(1)
        sudo('tail -f /var/log/%s/%s' % (self._service_name, log_name), user=self._user, group=self._group)

    def _track_event(self, event):
        """
        Track who deployed what service and what the release dir is to Graphite's events UI
        """
        if not self._graphite_host:
            print red('unable to track deployment event in graphite, no graphite host configured in ~/.mendel.conf')
            return

        url = 'http://%s/events/' % self._graphite_host

        user = getpass.getuser()
        what = '%s %s %s on host %s' % (user, event, self._service_name, env.host_string)
        data = ''
        tag_strs = (self._service_name, event)
        tags = ' '.join(tuple(str(_) for _ in tag_strs))

        data = {'what': what, 'tags': tags, 'data': data}
        r = urllib2.urlopen(url, json.dumps(data))
        if r.code != 200:
            print red('Unable to track deployment event in graphite (HTTP %s)' % r.code)

    def get_tasks(self):
        return [
            WrappedCallableTask(lcd_task(task, self._cwd))
            for task in
            [
                self.upload,
                self.deploy,
                self.install,
                self.build,
                self.tail,
                self.rollback,
                self.upstart,
                self.link_latest_release
            ]
        ]

