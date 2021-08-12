# Author-y4cj4sul3
# Description-This is a emaple of how to install third-party python packages to Fusion 360 python executable.
import logging
import logging.config
import os

import adsk.core
import adsk.fusion
import adsk.cam
import traceback

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger('mylogger')


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Setup logger

        # sol 1: add manually
        # logger.hasHandlers won't work since it also checks parent loggers
        if len(logger.handlers) == 0:
            # formatter
            formatter = logging.Formatter('%(asctime)s %(name)s$ [%(levelname)s]: %(message)s')
            # handler
            log_path = os.path.join(CURRENT_PATH, 'mylogger.log')
            file_handler = logging.FileHandler(filename=log_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            # logger
            logger.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)

        # # sol 2: by dictConfig
        # conf_path = os.path.join(CURRENT_PATH, 'config.yaml')
        # with open(conf_path, 'r', encoding='utf-8') as fp:
        #     config = yaml.load(fp)
        #     logging.config.dictConfig(config)
        #     logger = logging.getLogger('mylogger')

        # # sol 3: by fileConfig (will replace root)
        # # store original root logger
        # loggers = 'loggers:\n'+ '\n'.join(logging.root.manager.loggerDict)
        # root_logger = logging.getLogger('root')
        # ui.messageBox(loggers)
        # ui.messageBox(str(root_logger.handlers))
        # conf_path = os.path.join(CURRENT_PATH, 'logging.conf')
        # log_path = os.path.join(CURRENT_PATH, 'mylogger.log')
        # logging.config.fileConfig(conf_path, defaults={'fname': log_path}, disable_existing_loggers=False)
        # # logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mylogger.log'), level=logging.DEBUG)
        # logger = logging.getLogger('mylogger')

        # # fh = logging.FileHandler(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mylogger.log'))
        # # fh.setLevel(logging.DEBUG)
        # # logger.addHandler(fh)

        # ui.messageBox('mylogger handlers:\n' + str(logger.handlers))
        # logger.debug(loggers)
        logger.info('Initializing add-in ...')

        # try import packages
        try:
            logger.info('Try to import package')
            import numpy as np

            # logger.info("Installed Successfully.")

        except:
            logger.info("Try to install packages.")
            # install packages
            from .package_manager import install_package

            # use absolute path
            req_file_path = os.path.join(CURRENT_PATH, 'requirements.txt')
            install_package(req_file_path)

            # try import again
            try:
                logger.info('Try to import commands again')
                import numpy as np
            except:
                logger.error("Failed to import commands")
                raise

        logger.info('Add-in started')

        ui.messageBox(str(np.array([1, 2, 3])))

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            logger.error('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        logger.info('Add-in stopped')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            logger.error('Failed:\n{}'.format(traceback.format_exc()))
