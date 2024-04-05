from .get_certificate_data import GetCertificateData
from .bookmark_handler import BookmarkHandler
from .ReadCertExpiryConfig import ReadCertExpiryConfig
from .email_handler import EmailHandler
from .ServerResponseHandler import ServerResponseHandler
from CertExpiryLogger import CertExpiryLogger
from .MessageDirectory import MessageDictionary

GetCertificateData = GetCertificateData()
BookmarkHandler = BookmarkHandler()
config_reader = ReadCertExpiryConfig()
EmailHandler = EmailHandler()
ServerResponseHandler = ServerResponseHandler()
cert_expiry_logger = CertExpiryLogger()
messageHandler = MessageDictionary()
