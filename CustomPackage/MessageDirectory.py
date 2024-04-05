##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: MessageDirectory
# Description: This is the class which will hold the
#               messages used by this tool.
#
##########################################################################
"""MessageDictionary"""


class MessageDictionary:

    EmailTemplateMissing = (
        'Hello,\n\n'
        'This is to notify you that WxCCE Expiry notification {} Email'
        ' Template missing in the processing node, hence email notification'
        ' is disabled.\n\n'
        'Action : Check the logs for any issues in current run as email '
        'notification is currently disabled. Fix the missing email template'
        ' and re-trigger the certificate expiry processing job.\n\n'
        'Regards,\n'
        'Certificates Monitoring Service.')

    InternalEmailTemplateMissing = EmailTemplateMissing.format("Internal")
    ExternalEmailTemplateMissing = EmailTemplateMissing.format("External")
    BothEmailTemplatesMissing = EmailTemplateMissing.\
        format("Internal and External")
