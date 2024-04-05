##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: cert_expiry_utility
# Description: This class contains utility functions used by cert expiry
#               notification process.
#
###########################################################################
"""CertExpiryUtility Class"""

import datetime
import globalSetting
from CustomPackage.email_handler import EmailHandler
import csv
import os
import logging


class CertExpiryUtility:
    @staticmethod
    def get_cn_from_subject(subject):
        parts = subject.split(', ')
        for part in parts:
            if part.startswith("CN="):
                return part[3:]
        return "Unknown"

    @staticmethod
    def get_bucket_for_expiry(days_until_expiry):
        if days_until_expiry >= 91:
            return "Queued"
        elif days_until_expiry >= 61:
            return "90"
        elif days_until_expiry >= 31:
            return "60"
        elif days_until_expiry >= 8:
            return "30"
        elif days_until_expiry >= 2:
            return "7"
        elif days_until_expiry == 1:
            return "1"
        elif days_until_expiry <= 0:
            return "0"
        else:
            return "Error"

    @staticmethod
    def is_notification_enabled(bucket):
        notification_durations = globalSetting.confData.get(
            'notification_duration', {})
        return notification_durations.get(bucket, True)

    @staticmethod
    def get_days_until_expiry(expiry_date_str):
        if not expiry_date_str:
            return None
        try:
            expiry_date = datetime.datetime.strptime(
                expiry_date_str.split('T')[0], "%Y-%m-%d")
            current_date = datetime.datetime.now()
            time_difference = expiry_date - current_date
            days_until_expiry = time_difference.days
            return days_until_expiry
        except ValueError:
            return None

    @staticmethod
    def check_expiry_and_send_email():
        bookmark_notified_certs = []
        bookmark_data = CertExpiryUtility.load_bookmark_data()
        if bookmark_data is None:
            return
        expired_cert_notify_only_once = globalSetting.confData.get(
            'expired_cert_notify_only_once', 'yes')

        for cid, cert_info in bookmark_data.items():
            status = cert_info.get('Status')
            bucket = cert_info.get('Bucket')
            if status in ['Revoked', 'Renewed']:
                continue
            elif bucket == "Queued":
                continue

            if CertExpiryUtility.is_notification_enabled(bucket):
                if cert_info["Notified"] == "N":
                    EmailHandler.trigger_email_for_cert_expiry(cert_info)
                    bookmark_notified_certs.append(cert_info)
                    cert_info["Notified"] = "Y"
                elif cert_info["Notified"] == "Y" and bucket == "0" and \
                        expired_cert_notify_only_once == "no":
                    EmailHandler.trigger_email_for_cert_expiry(cert_info)
                    bookmark_notified_certs.append(cert_info)
        return bookmark_notified_certs

    @staticmethod
    def load_bookmark_data():
        bookmark_data = {}
        bookmark_path = "bookmark.csv"
        if os.path.exists(bookmark_path):
            with open(bookmark_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    bookmark_data[row["CID"]] = row
            return bookmark_data
        else:
            logging.info(
                "Bookmark not available, email notification for cert expiry"
                " is not processed.")
            return None
