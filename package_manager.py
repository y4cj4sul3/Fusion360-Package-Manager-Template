import logging
import os
# import sys
# import site
import platform
import subprocess

logger = logging.getLogger('mylogger.package_installer')


def install_package(requirements_file):
    logger.debug(f'Requirements file path: {requirements_file}')

    if not os.path.exists(requirements_file):
        logger.error(f'Requirements file not exists: {requirements_file}')
        raise FileNotFoundError(f'Requirement file not exists: {requirements_file}')

    # Get environment varible settings
    env = get_env()
    logger.debug(f'env PATH: {env["PATH"]}')

    # Import pip
    try:
        import pip
    except:
        # install pip
        # path to temporary store get-pip.py
        get_pip_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'get-pip.py')

        # TODO: detect any failure here
        # download and run get-pip.py to install pip
        commands = [
            'curl https://bootstrap.pypa.io/get-pip.py -o "' + get_pip_path + '"',
            'python "' + get_pip_path + '"',
            'python -m pip list',
        ]
        execute_external_command(commands, env=env)

        # try import pip again
        try:
            import pip
            logger.info('Install pip successfully')
        except:
            logger.error('Failed to install pip')
            raise

    # Upgrade pip to the lastest version
    # TODO: should make this an optional function? or force user specify pip version in requirements file?
    logger.info('Upgrade pip')
    logger.info(f'Original pip version: { pip.__version__}')
    # upgrade pip
    execute_external_command(['python -m pip install --upgrade pip', 'python -m pip install pip==random'], env=env)
    # execute_external_command(['python -m pip list'], env=env)
    # reimport to update package
    import importlib
    importlib.reload(pip)
    logger.info(f'Upgraded pip version: { pip.__version__}')

    # Install required dependency

    # Method 1: pip.main
    # This is a internal function of pip and it doesn't seems to report installation result
    # if hasattr(pip, 'main'):
    #     pip.main(['install', '-r', requirements_file])
    # elif hasattr(pip, '_internal') and hasattr(pip._internal, 'main'):
    #     pip._internal.main(['install', '-r', requirements_file])

    # Method 2: pip install -r
    # This may failed to install some of the packages
    # execute_external_command([f'python -m pip install -r "{requirements_file}"'], env=env)

    # Method 3: pip install line by line
    with open(requirements_file, 'r') as fp:
        for line in fp.readlines():
            execute_external_command([f'python -m pip install --user {line}'], env=env)

    # TODO: may have to detect failure
    execute_external_command(['python -m pip list'], env=env)
    logger.info('Install package successfully')


def execute_external_command(commands, env=None, block=False):
    # It seems that Windows can only do one command at a time
    if type(commands) == str:
        commands = [commands]

    for command in commands:
        # set environment variable
        if env is None:
            env = os.environ.copy()

        # execute external command
        # try:
        #     process = subprocess.run(command.split(' '), env=env, shell=True, stdout=subprocess.PIPE, check=True)
        # except subprocess.CalledProcessError:
        #     logger.debug(process.stdout.decode().strip())
        #     if process.stderr is not None:
        #         logger.debug(process.stderr.decode().strip())

        logger.debug('$ ' + command)

        process = subprocess.Popen(command, env=env, shell=True, stdout=subprocess.PIPE)
        if block:
            # this will wait until command finished
            stdout, stderr = process.communicate()
            logger.debug(stdout.decode().strip())
            if stderr is not None:
                logger.error(stderr.decode().strip())
        else:
            logs = []
            for line in process.stdout.readlines():
                logs.append(line.decode().strip())
            logger.debug('\n'.join(logs))

        logger.debug(f'return code: {process.returncode}')


def get_env():
    # python path
    # for adding to environment variable
    # python_path = ''
    # solution 1: sys.executable (unreliable, somwtimes it is relative path or refers to the Fusion 360 app)
    # exe_path = os.path.realpath(sys.executable)
    # if os.path.basename(exe_path).lower().startswith('python') and os.path.exists(exe_path):
    #     python_path = os.path.dirname(exe_path)
    # else:
    #     # solution 2: site.getsitepackage (unreliable, sometimes it is empty)
    #     site_paths = site.getsitepackages()
    #     if len(site_paths) > 0:
    #         python_path = site_paths[0].rsplit('lib')[0]

    # solution 3: by package path (most realiable)
    python_path = os.path.realpath(os.__file__).rsplit('lib')[0]

    # detect OS type
    OS = platform.system()
    if OS == 'Windows':
        PATH_SEPARATOR = ';'
        exe_path = os.path.join(python_path, 'python.exe')
    else:
        PATH_SEPARATOR = ':'
        python_path = os.path.join(python_path, 'bin')
        exe_path = os.path.join(python_path, 'python')

    logger.debug(f'Operating system: {OS}')
    logger.debug(f'Python folder path: {python_path}')
    logger.debug(f'Python executable path: {exe_path}')

    if not os.path.exists(exe_path):
        logger.error(f'Failed to install Add-In. Cannot find python executable.')
        raise

    # add path to environment variables
    env = os.environ.copy()
    env['PATH'] = python_path + PATH_SEPARATOR + env['PATH']

    return env


if __name__ == '__main__':
    # Manually install/uninstall packages
    # Note that you may use other version of python to run this script
    # If there is any problem, better add the path of python Fusion 360 used to the environment variable and manually install/uninstall packages
    # Note that Fusion 360 will create a .env file which contants path to its python packages, which is NOT the path to python executable

    # change logger
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('root')

    # set env
    # TODO: modify python_path
    python_path = "absolute/path/to/your/python/executable/folder/"
    env = os.environ.copy()
    OS = platform.system()
    if OS == 'Windows':
        PATH_SEPARATOR = ';'
    else:
        PATH_SEPARATOR = ':'
    env['PATH'] = python_path + PATH_SEPARATOR + env['PATH']

    # e.g. install numpy
    commands = [
        'python -m pip uninstall numpy',
        'python -m pip list'
    ]
    execute_external_command(commands, env=env)
