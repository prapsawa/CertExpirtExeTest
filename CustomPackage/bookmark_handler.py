##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: bookmark_handler
# Description: Create and/or update the bookmark CSV file
#       CID : Unique STO Certificate ID of the issued certificate
#       Status : Current status of the certificate. Values can be
#       {Active, Expired}
#
###########################################################################
"""BookmarkHandler Class"""


import os
import logging
import sys
import pandas as pd
from cert_expiry_utility import CertExpiryUtility
from CustomPackage.email_handler import EmailHandler


class BookmarkHandler:
    def populate_bookmark(self, all_certificate_data):
        bookmark_path = "bookmark.csv"
        fieldnames = [
            "CID",
            "Status",
            "ExpiryDate",
            "Bucket",
            "CN",
            "SAN",
            "Notified"]

        try:
            if not os.path.exists(bookmark_path):
                existing_data = pd.DataFrame(columns=fieldnames)
            else:
                existing_data = pd.read_csv(bookmark_path)

            existing_data['CID'] = existing_data['CID'].astype(str)

            existing_cids = set(existing_data['CID'])

            new_certificates = []
            error_certificates = []

            for cert in all_certificate_data:
                cid = str(cert.get('certId', ''))
                if cid not in existing_cids:
                    not_after = cert.get('notAfter', '')
                    expiry_date_str = not_after.split('T')[0]

                    days_until_expiry = CertExpiryUtility.\
                        get_days_until_expiry(expiry_date_str)

                    if days_until_expiry is not None:
                        bucket = CertExpiryUtility.get_bucket_for_expiry(
                            days_until_expiry)

                        if bucket != "Error":
                            san_entries = cert.get('sans', [])
                            san_str = "[" + ";".join(san_entries) + \
                                "]" if san_entries else ""
                            new_certificates.append({
                                "CID": cid,
                                "Status": cert.get("status", ""),
                                "ExpiryDate": expiry_date_str,
                                "Bucket": bucket,
                                "CN": CertExpiryUtility.get_cn_from_subject
                                (cert.get('subject', '')),
                                "SAN": san_str,
                                "Notified": "N"
                            })
                        else:
                            logging.info(
                                "Error while determining the bucket for "
                                f"certificate : {cid}")
                            error_certificates.append(cid)
                    else:
                        logging.error(
                            "Error while calculating days remaining before"
                            f" cert expiry for {cid}.")
                        error_certificates.append(cid)

            new_data = pd.DataFrame(new_certificates)

            if not new_data.empty:
                if existing_data.empty:
                    existing_data = new_data
                else:
                    new_data = pd.DataFrame(
                        new_certificates, columns=existing_data.columns)
                    existing_data = pd.concat(
                        [existing_data, new_data], ignore_index=True)
                existing_data.sort_values(by=['ExpiryDate'], inplace=True)
                existing_data.to_csv(bookmark_path, index=False)
                logging.info("Bookmark updated with new certificates.")
            else:
                logging.info("No new certificates to add to the bookmark.")

            if error_certificates:
                logging.info(
                    "Internal email triggered for notifying the processing"
                    f" errors for CIDs : {error_certificates}")
                EmailHandler.trigger_internal_email(
                    f'Error while processing CIDs : {error_certificates}.')

        except Exception as e:
            logging.error(f"Error occurred while populating bookmark: {e}")
            logging.info('Certificate Expiry Notification tool ended')
            sys.exit()

    def update_notified_cert_entry(self, certificates_sent_email):
        bookmark_path = "bookmark.csv"
        if not os.path.exists(bookmark_path):
            logging.error(f"Bookmark file '{bookmark_path}' not found.")
            return

        try:
            df = pd.read_csv(bookmark_path)
            df.loc[df['CID'].astype(str).isin(
                certificates_sent_email), 'Notified'] = 'Y'
            df.to_csv(bookmark_path, index=False)

            self.log_bucket_for_certificates(certificates_sent_email, df)

        except Exception as e:
            logging.error(
                "Error while updating the notified cert entries in bookmark."
                f" Exception : {e}")
            logging.info('Certificate Expiry Notification tool ended')
            sys.exit()

    def move_certificates_to_new_bucket(self):
        bookmark_path = "bookmark.csv"
        if not os.path.exists(bookmark_path):
            logging.error(f"Bookmark file '{bookmark_path}' not found.")
            return
        existing_data = pd.read_csv(bookmark_path)

        try:
            existing_data['ExpiryDate'] = pd.to_datetime(
                existing_data['ExpiryDate'])

            for index, row in existing_data.iterrows():
                expiry_date_str = row['ExpiryDate'].strftime("%Y-%m-%d")
                days_until_expiry = CertExpiryUtility.get_days_until_expiry(
                    expiry_date_str)

                if days_until_expiry is None:
                    logging.error(
                        "Move Cert to New Bucket - Error while calculating "
                        f"days remaining before cert expiry for {row['cid']}."
                        " Skipped ")
                    continue
                else:
                    new_bucket = CertExpiryUtility.get_bucket_for_expiry(
                        days_until_expiry)

                if new_bucket == "Error":
                    logging.error(
                        "Move Cert to New Bucket - Error while calculating "
                        f"days remaining before cert expiry for {row['cid']}."
                        " Skipped ")
                    continue

                if new_bucket != row["Bucket"]:
                    logging.info(
                        f"Certificate {row['CID']} moved from bucket "
                        f"{row['Bucket']} to {new_bucket}")
                    existing_data.loc[index, 'Bucket'] = new_bucket
                    existing_data.loc[index, 'Notified'] = "N"

            existing_data.to_csv(bookmark_path, index=False)

        except Exception as e:
            logging.error(
                "Error while processing move certificates to new bucket in"
                f" bookmark. Exception : {e}.")
            logging.info('Certificate Expiry Notification tool ended')
            sys.exit()

    def log_bucket_for_certificates(self, certificate_ids, df):
        buckets = \
            df[df['CID'].astype(str).isin(
                certificate_ids)]['Bucket'].tolist()
        logging.info('Updated bookmark to capture email notifications '
                     f'sent for CID: {", ".join(certificate_ids)} '
                     f'and bucket: {buckets}')
