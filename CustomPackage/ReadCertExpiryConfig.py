##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: ReadCertExpiryConfig
# Description: This is the ReadCertExpiryConfig class which will read the
#               config file data and process the fields.
#
###########################################################################
"""ReadCertExpiryConfig"""

import json
import logging
import globalSetting


class ReadCertExpiryConfig:
    @staticmethod
    def config_load_json():
        try:
            with open('cert_expiry_config.json') as f:
                configuration_data = json.load(f)
                globalSetting.confData = configuration_data
                return configuration_data
        except FileNotFoundError as e:
            logging.error(f"Config file not found: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error("Config file is not a valid JSON,"
                          f" Decoding failed.{e}")
            return None

    @staticmethod
    def processing_json_load():
        try:
            configurationData = globalSetting.confData
            missing_data = []

            sender_email = configurationData.get('sender_email')
            if not sender_email or not isinstance(sender_email, str):
                logging.info(
                    'Config parameter sender_email is missing or invalid.')
                missing_data.append('sender_email')

            receiver_email = configurationData.get('receiver_email')
            if not receiver_email or not isinstance(receiver_email, str):
                logging.info(
                    'Config parameter receiver_email is missing or invalid.')
                missing_data.append('receiver_email')

            smtp_server = configurationData.get('smtp_server')
            if not smtp_server or not isinstance(smtp_server, str):
                logging.info(
                    'Config parameter smtp_server is missing or invalid.')
                missing_data.append('smtp_server')

            smtp_port = configurationData.get('smtp_port')
            if not smtp_port or not isinstance(smtp_port, int):
                logging.info(
                    'Config parameter smtp_port is missing or invalid.')
                missing_data.append('smtp_port')

            cert_endpoints = configurationData.get('cert_endpoints')
            if not cert_endpoints or not isinstance(cert_endpoints, dict):
                logging.info(
                    'Config parameter cert_endpoints is missing or invalid.')
                missing_data.append('cert_endpoints')
            else:
                previous_cert_endpoint = cert_endpoints.get(
                    'previous_cert_endpoint')
                if not previous_cert_endpoint or not isinstance(
                        previous_cert_endpoint, str):
                    logging.info(
                        'Config parameter previous_cert_endpoint is missing'
                        ' or invalid.')
                    missing_data.append('previous_cert_endpoint')

                current_cert_endpoint = cert_endpoints.get(
                    'current_cert_endpoint')
                if not current_cert_endpoint or not isinstance(
                        current_cert_endpoint, str):
                    logging.info(
                        'Config parameter current_cert_endpoint is missing'
                        ' or invalid.')
                    missing_data.append('current_cert_endpoint')

            api_key = configurationData.get('api_key')
            if not api_key or not isinstance(api_key, str):
                logging.info('Config parameter api_key is missing'
                             ' or invalid.')
                missing_data.append('api_key')

            debugLogLevel = configurationData.get('debugLogLevel')
            if not debugLogLevel or not isinstance(debugLogLevel, int):
                logging.info(
                    'Config parameter debugLogLevel is missing'
                    ' or invalid. Proceeding with default value: 0 (INFO).')

            internal_team_email = configurationData.get(
                'internal_team_email')
            if not internal_team_email or not isinstance(
                    internal_team_email, str):
                logging.info(
                    'Config parameter internal_email_alias is missing'
                    ' or invalid.')
                missing_data.append('internal_team_email')

            expired_cert_notify_only_once = configurationData.get(
                'expired_cert_notify_only_once')
            if not expired_cert_notify_only_once or not isinstance(
                    expired_cert_notify_only_once, str):
                logging.info(
                    'Config parameter expired_cert_notify_only_once is'
                    ' missing or invalid. Proceeding with default value: yes.')

            notification_duration = configurationData.get(
                'notification_duration')
            if not notification_duration or not isinstance(
                    notification_duration, dict):
                logging.info(
                    'Config parameter notification_duration is missing'
                    ' or invalid. Proceeding with default value: True for'
                    ' all supported notification duration')

            max_retries = configurationData.get(
                'max_retries')
            if not max_retries or not isinstance(
                    max_retries, str):
                logging.info(
                    'Config parameter max_retries is'
                    ' missing or invalid. Proceeding with default value: 3.')

            if missing_data:
                logging.error('Mandatory config parameters either missing '
                              'in the config file or not having expected '
                              'values. Refer below list of config parameters '
                              'which need to be updated.')
                logging.info('Missing parameters: {}'.format(missing_data))
                return None

            return configurationData

        except FileNotFoundError as err:
            logging.error('Configuration file not found in the path')
            logging.error(err)
            return None
