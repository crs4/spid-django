from spiddjango import SPID_ATTRIBUTES

MAP = {
    "identifier": "urn:oasis:names:tc:SAML:2.0:attrname-format:basic",
    "fro": {
        spid_attr: spid_attr for spid_attr in SPID_ATTRIBUTES
    },
    "to": {
        spid_attr: spid_attr for spid_attr in SPID_ATTRIBUTES
    }
}
