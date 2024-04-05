##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: CertExpiryLogger
# Description: This is the CertExpiryLogger file which will perform logging.
#
###########################################################################
"""CertExpiryLogger Class"""

import os
import logging as Logging
from logging.handlers import RotatingFileHandler


class CertExpiryLogger:
    def __init__(self) -> None:
        try:
            global log_handler, log_formatter
            log_dir = "log"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            log_file = os.path.join(log_dir, "cert_expiry_notification.log")
            log_handler = RotatingFileHandler(
                log_file,
                maxBytes=10000000,
                backupCount=20,
            )
            log_formatter = Logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            log_handler.setFormatter(log_formatter)
        except PermissionError:
            print("Permission denied while creating log directory.")
            exit(1)

    def configure_logging(self, log_level):
        logger = Logging.getLogger('')
        logger.setLevel(log_level)
        logger.addHandler(log_handler)
        return logger
