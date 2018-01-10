import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf import settings

from spiddjango import SPID_ATTRIBUTES

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from saml2 import saml
import saml2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPID_ATTRIBUTE_CONSUMING_SERVICE = getattr(settings, 'SPID_ATTRIBUTE_CONSUMING_SERVICE', '1')
SPID_METADATA_DIR = getattr(settings, 'SPID_METADATA_DIR', None)
SPID_ATTRIBUTE_MAPPING = getattr(settings, 'SAML_ATTRIBUTE_MAPPING', {
    "spidCode": ('spid_code',),
    "name": ('first_name',),
    "gender": ('gender',),
    "ivaCode": ('iva_code',),
    "placeOfBirth": ('place_of_birth',),
    "companyName": ('company_name',),
    "mobilePhone": ('mobile_phone',),
    "expirationDate": ('expiration_date',),
    "address": ('address',),
    "digitalAddress": ('digital_address',),
    "email": ('email',),
    "registeredOffice": ('registered_office',),
    "idCard": ('id_card',),
    "dateOfBirth": ('date_of_birth',),
    "countyOfBirth": ('county_of_birth',),
    "familyName": ('last_name',),
    "fiscalNumber": ('username',),
})

ROOT_URL = getattr(settings, 'ROOT_URL')
SAML_SP_NAME = getattr(settings, 'SAML_SP_NAME')
SAML_SP_KEY_PATH = getattr(settings, 'SAML_SP_KEY_PATH')
SAML_SP_CRT_PATH = getattr(settings, 'SAML_SP_CRT_PATH')

SPID_REQUESTED_ATTRIBUTES = getattr(settings, 'SPID_REQUESTED_ATTRIBUTES', SPID_ATTRIBUTES)
SPID_REQUIRED_ATTRIBUTES = getattr(settings, 'SPID_REQUIRED_ATTRIBUTES', SPID_ATTRIBUTES)
METADATA_DIR = os.path.join(os.path.dirname(__file__), 'spid-idp-metadata/')
ATTRIB_MAP_DIR_PATH = os.path.join(os.path.dirname(__file__), './saml2/attribute-maps')

idp_metadata_files = [os.path.join(METADATA_DIR, f) for f in os.listdir(METADATA_DIR)]
if SPID_METADATA_DIR is not None:
    idp_metadata_files.extend([f for f in os.listdir(SPID_METADATA_DIR) if
                               os.path.isfile(os.path.join(SPID_METADATA_DIR, f) and f.endswith('.xml'))])

SPID_SAML_CONFIG = {
    'xmlsec_binary': '/usr/bin/xmlsec1',
    'entityid': urljoin(ROOT_URL, '/saml2/metadata/'),
    'attribute_map_dir': ATTRIB_MAP_DIR_PATH,
    'service': {
        'sp': {
            'allow_unsolicited': True,
            'logout_requests_signed': True,
            'authn_requests_signed': True,
            'want_response_signed': True,
            'name': SAML_SP_NAME,
            'name_id_format': saml.NAMEID_FORMAT_TRANSIENT,
            'requested_attributes': [{
                'name': spid_attr,
                'name_format': 'urn:oasis:names:tc:SAML:2.0:attrname-format:basic'
            } for spid_attr in SPID_REQUESTED_ATTRIBUTES],
            'required_attributes': SPID_REQUIRED_ATTRIBUTES,
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    (urljoin(ROOT_URL, '/saml2/acs/'), saml2.BINDING_HTTP_POST),
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                'single_logout_service': [
                    (urljoin(ROOT_URL, '/saml2/ls/'), saml2.BINDING_HTTP_REDIRECT),
                    (urljoin(ROOT_URL, '/saml2/ls/post/'), saml2.BINDING_HTTP_POST),
                ],
            },

        }
    },
    # where the remote metadata is stored
    'metadata': {
        'local': idp_metadata_files,
    },
    # set to 1 to output debugging information
    'debug': 1 if settings.DEBUG is True else 0,
    'timeslack': 5000,
    'accepted_time_diff': 5000,

    # certificate
    'key_file': SAML_SP_KEY_PATH,  # private part
    'cert_file': SAML_SP_CRT_PATH,  # public part
    'valid_for': 24 * 365,  # how long is our metadata valid
}
