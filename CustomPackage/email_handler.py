##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: email_handler
# Description: Handles certificate expiry email notification trigger and
#              internal email notification trigger for issues with
#              certificate expiry backend process.
#
###########################################################################
"""EmailHandler Class"""

import smtplib
from email.mime.text import MIMEText
import globalSetting
import logging
from datetime import datetime
import os
from CustomPackage.MessageDirectory import MessageDictionary


class EmailHandler:
    @staticmethod
    def load_email_template(template_file):
        try:
            with open(template_file, 'r') as file:
                template = file.read()
            return template
        except FileNotFoundError:
            return None

    @staticmethod
    def trigger_internal_email(failure_reason):

        if globalSetting.internal_email_template_missing:
            return

        sender_email = \
            globalSetting.confData['sender_email']
        receiver_email = \
            globalSetting.confData['internal_team_email']
        smtp_server = \
            globalSetting.confData['smtp_server']
        smtp_port = \
            globalSetting.confData['smtp_port']
        template_file = \
            "./EmailTemplates/Cert_Expiry_Internal_Email_Template.txt"
        template = \
            EmailHandler.load_email_template(template_file)

        current_date = datetime.now().strftime('%Y-%m-%d')
        subject = (
            "ACTION REQUIRED: WxCCE Certificate Expiry Notification"
            "job reported an issue on {DATE}".format(
                DATE=current_date)
        )
        message = template.replace(
            '{DATE}', current_date).replace(
            '{InternalEmailReason}', failure_reason)

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(sender_email, receiver_email, msg.as_string())
                logging.info(
                    "Email triggered to internal "
                    "certificate expiry job monitoring team. "
                    f"Reason : {failure_reason}")
        except smtplib.SMTPException:
            logging.error(
                "Exception during processing of send internal email for "
                f"{failure_reason}.")

    @staticmethod
    def trigger_email_for_cert_expiry(cert_info):

        if globalSetting.external_email_template_missing:
            return
        sender_email = globalSetting.confData['sender_email']
        receiver_email = globalSetting.confData['receiver_email']
        smtp_server = globalSetting.confData['smtp_server']
        smtp_port = globalSetting.confData['smtp_port']
        template_file = \
            "./EmailTemplates/Cert_Expiry_Notification_Email_Template.txt"
        template = EmailHandler.load_email_template(template_file)

        subject = (
            "ACTION REQUIRED: SSL Certificate Request {CID} for {CN} "
            "Expiring in {X} days".format(
                CID=cert_info['CID'],
                CN=cert_info['CN'],
                X=cert_info['Bucket']))

        if 'SAN' in cert_info and cert_info['SAN']:
            san_text = ''.join(cert_info['SAN']) + '\n'
            message = template.replace(
                '{CID}', cert_info['CID']
            ).replace(
                '{CN}', cert_info['CN']
            ).replace(
                '{X}', cert_info['Bucket']
            ).replace(
                '{SANs}', f"The SANs associated with this request are: "
                f"{san_text}"
            )
        else:
            message = template.replace(
                '{CID}', cert_info['CID']
            ).replace(
                '{CN}', cert_info['CN']
            ).replace(
                '{X}', cert_info['Bucket']
            ).replace(
                '{SANs}', ''
            )

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(sender_email, receiver_email, msg.as_string())
                logging.info(
                    "Email sent for certificate ID: {}".format(
                        cert_info['CID']))
        except smtplib.SMTPException:
            logging.error(
                "Exception during processing of send external email for "
                f"CID: {cert_info['CID']}.")

    def send_internal_email(message):
        sender_email = globalSetting.confData['sender_email']
        receiver_email = globalSetting.confData['internal_team_email']
        smtp_server = globalSetting.confData['smtp_server']
        smtp_port = globalSetting.confData['smtp_port']

        subject = ("ACTION REQUIRED: WxCCE Expiry notification Email "
                   "Template missing")
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(sender_email, receiver_email, msg.as_string())
                logging.info("Internal email triggered for missing "
                             "template.")
        except smtplib.SMTPException as e:
            logging.error(
                "Exception while sending internal email for missing template."
                f" Exception : {e}")

    @staticmethod
    def check_for_email_template():
        internal_template_path = \
            "./EmailTemplates/Cert_Expiry_Internal_Email_Template.txt"
        external_template_path = \
            "./EmailTemplates/Cert_Expiry_Notification_Email_Template.txt"

        internal_missing = not os.path.exists(internal_template_path)
        external_missing = not os.path.exists(external_template_path)

        if external_missing and internal_missing:
            logging.error("Both Email Templates Missing")
            globalSetting.internal_email_template_missing = True
            globalSetting.external_email_template_missing = True
            EmailHandler.send_internal_email(
                MessageDictionary.BothEmailTemplatesMissing)

        elif internal_missing:
            logging.error("Internal Email Template is Missing.")
            globalSetting.internal_email_template_missing = True
            EmailHandler.send_internal_email(
                MessageDictionary.InternalEmailTemplateMissing)
        elif external_missing:
            logging.error("External Email Template Missing")
            globalSetting.external_email_template_missing = True
            EmailHandler.send_internal_email(
                MessageDictionary.ExternalEmailTemplateMissing)
        else:
            globalSetting.internal_email_template_missing = False
            globalSetting.external_email_template_missing = False
