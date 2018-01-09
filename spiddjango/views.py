import base64
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.utils.http import is_safe_url
from django.utils.six import text_type, binary_type
from djangosaml2.cache import OutstandingQueriesCache
from djangosaml2.conf import get_config
from djangosaml2.overrides import Saml2Client
from djangosaml2.utils import available_idps, get_location, get_idp_sso_supported_bindings, get_custom_setting
from djangosaml2.views import callable_bool
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from saml2.s_utils import UnsupportedBinding
from saml2.xmldsig import SIG_RSA_SHA1, SIG_RSA_SHA256

from spiddjango.settings import DEFAULT_ATTRIBUTE_CONSUMING_SERVICE

logger = logging.getLogger('spiddjango')


def login(request,
          config_loader_path=None,
          wayf_template='wayf.html',
          authorization_error_template='djangosaml2/auth_error.html',
          post_binding_form_template='djangosaml2/post_binding_form.html'):
    """SAML Authorization Request initiator
    This view initiates the SAML2 Authorization handshake
    using the pysaml2 library to create the AuthnRequest.
    It uses the SAML 2.0 Http Redirect protocol binding.
    * post_binding_form_template - path to a template containing HTML form with
    hidden input elements, used to send the SAML message data when HTTP POST
    binding is being used. You can customize this template to include custom
    branding and/or text explaining the automatic redirection process. Please
    see the example template in
    templates/djangosaml2/example_post_binding_form.html
    If set to None or nonexistent template, default form from the saml2 library
    will be rendered.
    """
    logger.debug('Login process started')

    came_from = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    if not came_from:
        logger.warning('The next parameter exists but is empty')
        came_from = settings.LOGIN_REDIRECT_URL

    # Ensure the user-originating redirection url is safe.
    if not is_safe_url(url=came_from, host=request.get_host()):
        came_from = settings.LOGIN_REDIRECT_URL

    # if the user is already authenticated that maybe because of two reasons:
    # A) He has this URL in two browser windows and in the other one he
    #    has already initiated the authenticated session.
    # B) He comes from a view that (incorrectly) send him here because
    #    he does not have enough permissions. That view should have shown
    #    an authorization error in the first place.
    # We can only make one thing here and that is configurable with the
    # SAML_IGNORE_AUTHENTICATED_USERS_ON_LOGIN setting. If that setting
    # is True (default value) we will redirect him to the came_from view.
    # Otherwise, we will show an (configurable) authorization error.
    if callable_bool(request.user.is_authenticated):
        redirect_authenticated_user = getattr(settings, 'SAML_IGNORE_AUTHENTICATED_USERS_ON_LOGIN', True)
        if redirect_authenticated_user:
            return HttpResponseRedirect(came_from)
        else:
            logger.debug('User is already logged in')
            return render(request, authorization_error_template, {
                'came_from': came_from,
            })

    selected_idp = request.GET.get('idp', None)
    conf = get_config(config_loader_path, request)

    # is a embedded wayf needed?
    idps = available_idps(conf, 'it')
    if selected_idp is None and len(idps) > 1:
        logger.debug('A discovery process is needed')
        return render(request, wayf_template, {
            'available_idps': idps,
            'came_from': came_from,
        })

    # choose a binding to try first
    sign_requests = getattr(conf, '_sp_authn_requests_signed', False)
    binding = BINDING_HTTP_POST if sign_requests else BINDING_HTTP_REDIRECT
    logger.debug('Trying binding %s for IDP %s', binding, selected_idp)

    # ensure our selected binding is supported by the IDP
    supported_bindings = get_idp_sso_supported_bindings(selected_idp, config=conf)
    if binding not in supported_bindings:
        logger.debug('Binding %s not in IDP %s supported bindings: %s',
                     binding, selected_idp, supported_bindings)
        if binding == BINDING_HTTP_POST:
            logger.warning('IDP %s does not support %s,  trying %s',
                           selected_idp, binding, BINDING_HTTP_REDIRECT)
            binding = BINDING_HTTP_REDIRECT
        else:
            logger.warning('IDP %s does not support %s,  trying %s',
                           selected_idp, binding, BINDING_HTTP_POST)
            binding = BINDING_HTTP_POST
        # if switched binding still not supported, give up
        if binding not in supported_bindings:
            raise UnsupportedBinding('IDP %s does not support %s or %s',
                                     selected_idp, BINDING_HTTP_POST, BINDING_HTTP_REDIRECT)

    client = Saml2Client(conf)
    http_response = None
    attribute_consuming_service_index = get_custom_setting('SPID_ATTRIBUTE_CONSUMING_SERVICE',
                                                     DEFAULT_ATTRIBUTE_CONSUMING_SERVICE)

    logger.debug('Redirecting user to the IdP via %s binding.', binding)
    if binding == BINDING_HTTP_REDIRECT:
        try:
            # do not sign the xml itself, instead use the sigalg to
            # generate the signature as a URL param
            sig_alg_option_map = {'sha1': SIG_RSA_SHA1,
                                  'sha256': SIG_RSA_SHA256}
            sig_alg_option = getattr(conf, '_sp_authn_requests_signed_alg', 'sha1')
            sigalg = sig_alg_option_map[sig_alg_option] if sign_requests else None
            session_id, result = client.prepare_for_authenticate(
                entityid=selected_idp, relay_state=came_from,
                binding=binding, sign=False, sigalg=sigalg,
                attribute_consuming_service_index=attribute_consuming_service_index)
        except TypeError as e:
            logger.error('Unable to know which IdP to use')
            return HttpResponse(text_type(e))
        else:
            http_response = HttpResponseRedirect(get_location(result))
    elif binding == BINDING_HTTP_POST:
        if post_binding_form_template:
            # get request XML to build our own html based on the template
            try:
                location = client.sso_location(selected_idp, binding)
            except TypeError as e:
                logger.error('Unable to know which IdP to use')
                return HttpResponse(text_type(e))
            session_id, request_xml = client.create_authn_request(
                location,
                binding=binding,
                attribute_consuming_service_index=attribute_consuming_service_index)
            try:
                http_response = render(request, post_binding_form_template, {
                    'target_url': location,
                    'params': {
                        'SAMLRequest': base64.b64encode(binary_type(request_xml, 'UTF-8')),
                        'RelayState': came_from,
                    },
                })
            except TemplateDoesNotExist:
                pass

        if not http_response:
            # use the html provided by pysaml2 if no template was specified or it didn't exist
            try:
                session_id, result = client.prepare_for_authenticate(
                    entityid=selected_idp, relay_state=came_from,
                    binding=binding, attribute_consuming_service_index=attribute_consuming_service_index)
            except TypeError as e:
                logger.error('Unable to know which IdP to use')
                return HttpResponse(text_type(e))
            else:
                http_response = HttpResponse(result['data'])
    else:
        raise UnsupportedBinding('Unsupported binding: %s', binding)

    # success, so save the session ID and return our response
    logger.debug('Saving the session_id in the OutstandingQueries cache')
    oq_cache = OutstandingQueriesCache(request.session)
    oq_cache.set(session_id, came_from)
    return http_response
