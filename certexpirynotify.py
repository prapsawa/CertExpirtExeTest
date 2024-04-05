##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: certexpirynotify
# Description: This is the Certificate Expiry Notification Job backend
#          code which will perform below operations.
#       a)Initialise logging framework and parse the config file for
#          processing.
#       b)Fetch the certificates from Cisco STO using the API's for
#          all the configured endpoints.
#       c)Process the list of certificates and identify the certificates
#           to be notified for expiry.
#       d)Send certificate expiry email notification for expired and going
#           to expire in next X days.
#       e)Bookmark the notified certificates to avoid multiple unexpected
#           notification.
#
###########################################################################


import globalSetting
import logging as Logging
from CustomPackage import GetCertificateData, BookmarkHandler
from CustomPackage import config_reader, cert_expiry_logger
from CustomPackage import EmailHandler
from cert_expiry_utility import CertExpiryUtility
import sys


def CertExpiryNotification():
    try:
        EmailHandler.check_for_email_template()
        all_certificate_data = GetCertificateData.\
            get_cert_data_for_configured_endpoints()
        BookmarkHandler.populate_bookmark(all_certificate_data)
        BookmarkHandler.move_certificates_to_new_bucket()

        internal_email_template_missing = \
            globalSetting.internal_email_template_missing
        external_email_template_missing = \
            globalSetting.external_email_template_missing

        if not (internal_email_template_missing or
                external_email_template_missing):
            bookmark_notified_certs = \
                CertExpiryUtility.check_expiry_and_send_email()
            if not bookmark_notified_certs:
                logging.info("No certificates to notify.")
            else:
                logging.info("Certificates which is going to expiry has"
                             " been notified successfully.")
                cids_to_update = [cert['CID']
                                  for cert in bookmark_notified_certs]
                BookmarkHandler.update_notified_cert_entry(cids_to_update)

    except Exception as e:
        logging.error("Exception during Cert Expiry Notification "
                      f"processing. Exception : {e}")
        logging.info('Certificate Expiry Notification tool ended')
        sys.exit()


if __name__ == '__main__':
    globalSetting.init()
    logging = cert_expiry_logger.configure_logging(Logging.INFO)
    logging.info(
        'Certificate Expiry Notification Job backend process has started')
    logging.info('Logging started for Certificate Expiry Notification tool'
                 f' {globalSetting.version} ')

    try:
        config_data = config_reader.config_load_json()
        if not config_data:
            logging.error("Failed to load configuration data.")
            logging.info('Certificate Expiry Notification tool ended')
            sys.exit()
    except Exception as e:
        logging.error("An error occurred. "
                      f"Exception during loading configuration file: {e}")
        logging.info('Certificate Expiry Notification tool ended')
        sys.exit()

    try:
        config_data = config_reader.processing_json_load()
        if not config_data:
            logging.error("Failed to process configuration data. "
                          "Exiting the Cert Expiry processing.")
            logging.info('Certificate Expiry Notification tool ended')
            sys.exit()
    except Exception as e:
        logging.error(
            "An error occurred, Exception during processing"
            f"configuration file: " f"{e}")
        logging.info('Certificate Expiry Notification tool ended')
        sys.exit()

    debug_log_level = globalSetting.confData.get('debugLogLevel', 0)
    if debug_log_level == 1:
        logging = cert_expiry_logger.configure_logging(Logging.DEBUG)
    else:
        logging = cert_expiry_logger.configure_logging(Logging.INFO)

    CertExpiryNotification()
    logging.info('Certificate Expiry Notification tool ended')
