import random

from django import template
from django.conf import settings

register = template.Library()

SPID_BUTTON_SIZES = {'small', 'medium', 'large', 'xlarge'}
SPID_BUTTON_SIZES_SHORT = {'small': 's', 'medium': 'm', 'large': 'l', 'xlarge': 'xl'}


@register.inclusion_tag("spid-sp-access-button.html", takes_context=True)
def spid_button(context, size='medium'):
    if size not in SPID_BUTTON_SIZES:
        raise ValueError("argument 'size': value %r not in %r." % (size, SPID_BUTTON_SIZES))

    spid_idp_list = [
            {'id': 'arubaid', 'name': 'Aruba ID'},
            {'id': 'infocertid', 'name': 'Infocert ID'},
            {'id': 'namirialid', 'name': 'Namirial ID'},
            {'id': 'posteid', 'name': 'Poste ID'},
            {'id': 'sielteid', 'name': 'Sielte ID'},
            {'id': 'spiditalia', 'name': 'SPIDItalia Register.it'},
            {'id': 'timid', 'name': 'Tim ID'},
            {'id': 'test', 'name': 'Test'},
    ]

    return {
        'method': context['request'].method.lower(),
        'post_data': context['request'].POST,
        'button_size': size,
        'button_size_short': SPID_BUTTON_SIZES_SHORT[size],
        'idp_list': spid_idp_list
    }
