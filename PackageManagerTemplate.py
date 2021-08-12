# Author-y4cj4sul3
# Description-This is a emaple of how to install third-party python packages to Fusion 360 python executable.
import logging
import logging.config
import os
import traceback

import adsk.cam
import adsk.core
import adsk.fusion

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger('mylogger')


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Setup logger

        # sol 1: add manually
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

        logger.info('Initializing add-in ...')

        # try import packages
        try:
            logger.info('Try to import package')
            import numpy as np
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
