from django import template
from django.conf import settings
from djangosaml2.utils import available_idps
from djangosaml2.conf import get_config

register = template.Library()

SPID_BUTTON_SIZES = {'small', 'medium', 'large', 'xlarge'}
SPID_BUTTON_SIZES_SHORT = {'small': 's', 'medium': 'm', 'large': 'l', 'xlarge': 'xl'}
SPID_IDP_MAPPING = {
    'https://login.id.tim.it/affwebservices/public/saml2sso': ('timid', 'Tim ID'),
    'https://spid.register.it': ('spiditalia', 'SPIDItalia Register.it'),
    'https://idp.namirialtsp.com/idp': ('namirialid', 'Namirial ID'),
    'https://loginspid.aruba.it': ('arubaid', 'Aruba ID'),
    'https://posteid.poste.it': ('posteid', 'Poste ID'),
    'https://spid-testenv-identityserver': ('test', 'AGID Test'),
    'https://identity.sieltecloud.it': ('sielteid', 'Sielte ID'),
    'https://identity.infocert.it': ('infocertid', 'Infocert ID'),
}


@register.inclusion_tag("spid-sp-access-button.html", takes_context=True)
def spid_button(context, size='medium'):
    if size not in SPID_BUTTON_SIZES:
        raise ValueError("argument 'size': value %r not in %r." % (size, SPID_BUTTON_SIZES))

    spid_idp_list = []
    if 'available_idps' in context:
        idps = context['available_idps']
    else:
        conf = get_config(None, context['request'])
        idps = available_idps(conf, 'it')

    for idp in idps:
        if idp == 'https://spid-testenv-identityserver' and settings.DEBUG is False:
            continue
        try:
            spid_idp_list.append({'url': idp, 'id': SPID_IDP_MAPPING[idp][0], 'name': SPID_IDP_MAPPING[idp][1]})
        except KeyError:
            pass

    return {
        'method': 'get',
        'button_size': size,
        'button_size_short': SPID_BUTTON_SIZES_SHORT[size],
        'idp_list': spid_idp_list
    }
