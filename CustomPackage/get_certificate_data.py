##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: get_certificate_data
# Description: This is the get_certificate_data file which will perform
#              below operations
#   a)Contains logic for fetching certificate data from configured endpoints.
#   b)Email notification triggered to internal team for any certificate
#       fetching or processing issues.
#
###########################################################################
"""GetCertificateData Class"""
import requests
import logging
import time
import sys
import globalSetting
from CustomPackage.email_handler import EmailHandler
from CustomPackage.ServerResponseHandler import ServerResponseHandler


class GetCertificateData:
    @staticmethod
    def get_cert_data_for_configured_endpoints():
        all_certificate_data = []
        max_retries = globalSetting.confData.get('max_retries', 3)

        try:
            for endpoint, url in \
                    globalSetting.confData['cert_endpoints'].items(
                    ):
                truncated_url = url.split(".com")[0] + ".com"
                logging.info(
                    "Fetching the certificates "
                    f"from endpoint {truncated_url}")
                page_number = 0

                params = {"pageNumber": 0}
                response = requests.get(
                    url,
                    headers={
                        "Authorization": "SSLAPI api_key=\""
                        f"{globalSetting.confData['api_key']}\""},
                    params=params)
                total_pages = response.json().get("totalPages")

                while True:
                    params["pageNumber"] = page_number

                    response = requests.get(
                        url,
                        headers={
                            "Authorization": "SSLAPI api_key=\""
                            f"{globalSetting.confData['api_key']}\""},
                        params=params)

                    success, reason = \
                        ServerResponseHandler(
                        ).ServerResponseHandlerMethod(response)

                    if success:
                        certificate_data = response.json()
                        current_page_data = certificate_data.get("certs", [])
                        all_certificate_data.extend(current_page_data)

                        logging.info(
                            f"Fetched page {page_number}"
                            f" from {truncated_url}")

                        page_number += 1

                    elif response.status_code in [500, 502, 503, 504]:
                        retries = 0

                        while retries < max_retries:
                            logging.info("Retrying request for "
                                         f"({truncated_url}), Page "
                                         f"{page_number}, "
                                         f"Retry: {retries + 1}")
                            time.sleep(300)
                            response = requests.get(
                                url,
                                headers={
                                    "Authorization": "SSLAPI api_key=\""
                                    f"{globalSetting.confData['api_key']}\""},
                                params=params)
                            retry_success, retry_reason = \
                                ServerResponseHandler(
                                ).ServerResponseHandlerMethod(response)

                            if retry_success:
                                logging.info("Retry Succeeded for "
                                             f"({truncated_url}), Page "
                                             f"{page_number}, "
                                             f"Retry: {retries + 1}")
                                certificate_data = response.json()
                                current_page_data = certificate_data.get(
                                    "certs", [])
                                all_certificate_data.extend(current_page_data)
                                logging.info(
                                    f"Fetched page {page_number} from "
                                    f"{truncated_url}")
                                page_number += 1
                                break
                            retries += 1
                        else:
                            logging.error("Max retries reached for "
                                          f"({truncated_url}), stopping "
                                          "further processing for this "
                                          "endpoint")
                            EmailHandler.trigger_internal_email(
                                f'{retry_reason} received for '
                                f'{truncated_url}.')
                            break

                    else:
                        logging.error('Unexpected HTTP response from '
                                      f'({truncated_url}), Response received'
                                      f' is {response.status_code}')
                        EmailHandler.trigger_internal_email(
                            f"{reason} received for {truncated_url}.")
                        break

                    if page_number >= total_pages:
                        break

            return all_certificate_data

        except requests.exceptions.RequestException as e:
            reason = ("Exception while processing response from "
                      f"{truncated_url} for page number {page_number}."
                      f" Exception during processing : {e}")
            logging.error(reason)
            EmailHandler.trigger_internal_email(reason)
            logging.info('Certificate Expiry Notification tool ended')
            sys.exit()
