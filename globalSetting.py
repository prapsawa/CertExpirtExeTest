##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: globalSetting.py
# Description: This file initialises the global values.
#
###########################################################################

def init():
    global sender_email, receiver_email, internal_team_email
    global smtp_server, smtp_port
    global api_key, debugLogLevel, expired_cert_notify_only_once
    global cert_endpoints, notification_duration, max_retries, version
    global confData
    global internal_email_template_missing, external_email_template_missing

    sender_email = ""
    receiver_email = ""
    internal_team_email = ""
    smtp_server = ""
    smtp_port = ""
    api_key = ""
    debugLogLevel = 0
    expired_cert_notify_only_once = "yes"
    cert_endpoints = {
        "current_cert_endpoint": "",
        "previous_cert_endpoint": ""
    }
    notification_duration = {
        "0": True,
        "1": True,
        "7": True,
        "30": True,
        "60": True,
        "90": True
    }
    confData = {}
    max_retries = 3
    version = "[v1.0]"
    internal_email_template_missing = False
    external_email_template_missing = False
