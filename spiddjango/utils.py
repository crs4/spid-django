from os.path import isfile

from spiddjango import SPID_ATTRIBUTES

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from os import path, listdir
from saml2 import saml
import saml2

from spiddjango.settings import SPID_METADATA_DIR


METADATA_DIR = path.join(path.dirname(__file__), 'spid-idp-metadata/')
ATTRIB_MAP_DIR_PATH = path.join(path.dirname(__file__), './saml2/attribute-maps')


def get_saml_config(root_url, sp_name, sp_key_file, sp_cert_file, requested_attributes=SPID_ATTRIBUTES,
                    required_attributes=SPID_ATTRIBUTES):
    idp_metadata_files = [path.join(METADATA_DIR, f) for f in listdir(METADATA_DIR)]
    if SPID_METADATA_DIR is not None:
        idp_metadata_files.extend([f for f in listdir(SPID_METADATA_DIR) if
                                   isfile(path.join(SPID_METADATA_DIR, f) and f.endswith('.xml'))])

    return {
        'xmlsec_binary': '/usr/bin/xmlsec1',
        'entityid': urljoin(root_url, '/saml2/metadata/'),
        'attribute_map_dir': ATTRIB_MAP_DIR_PATH,
        'service': {
            'sp': {
                'allow_unsolicited': True,
                'logout_requests_signed': True,
                'authn_requests_signed': True,
                'want_response_signed': True,
                'name': sp_name,
                'name_id_format': saml.NAMEID_FORMAT_TRANSIENT,
                'requested_attributes': [{
                    'name': spid_attr,
                    'name_format': 'urn:oasis:names:tc:SAML:2.0:attrname-format:basic'
                } for spid_attr in requested_attributes],
                'required_attributes': required_attributes,
                'endpoints': {
                    # url and binding to the assetion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        (urljoin(root_url, '/saml2/acs/'), saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        (urljoin(root_url, '/saml2/ls/'), saml2.BINDING_HTTP_REDIRECT),
                        (urljoin(root_url, '/saml2/ls/post/'), saml2.BINDING_HTTP_POST),
                    ],
                },

            }
        },
        # where the remote metadata is stored
        'metadata': {
            'local': idp_metadata_files,
        },
        # set to 1 to output debugging information
        'debug': 1,
        'timeslack': 5000,
        'accepted_time_diff': 5000,

        # certificate
        'key_file': sp_key_file,  # private part
        'cert_file': sp_cert_file,  # public part
        'valid_for': 24 * 365,  # how long is our metadata valid
    }
