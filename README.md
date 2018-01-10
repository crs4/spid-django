# Description

spiddjango is a Django App that implements a SPID Service Provider. It is based on based on djangosaml2.

# Installation

To install the application just run 

```bash
python setup.py install
```

# Configuration

To use the application, these are the steps you need to perform:

In settings.py add to INSTALLED_APPS both djangosaml2 and spiddjango

```python
INSTALLED_APPS = [
    ...,
    'djangosaml2',
    'spiddjango'
]
```

Add `djangosaml2.backends.Saml2Backend` to AUTHENTICATION_BACKENDS

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
    ...
]
```

Set as user model 'spiddjango.SpidUser'
```python
AUTH_USER_MODEL = 'spiddjango.SpidUser'
```

Define the following attributes:

```python
SAML_SP_NAME = '<the name of the SP>' 
SAML_SP_KEY_PATH = '<path_of_the_key_file>'
SAML_SP_CRT_PATH = '<path_of_the_key_file>'
```

Import the attributes SPID_SAML_CONFIG and SPID_SAML_ATTRIBUTE_MAPPING and assign them
to SAML_CONFIG and SAML_ATTRIBUTE_MAPPING.

```python
from spiddjango.settings import SPID_SAML_CONFIG, SPID_ATTRIBUTE_MAPPING
SAML_CONFIG = SPID_SAML_CONFIG
SAML_ATTRIBUTE_MAPPING = SPID_ATTRIBUTE_MAPPING
```

These attributes are necessary for `djangosaml2`. They can also be customized but spiddjango provides
a configuration that works fine for SPID.

By default the SP is configured to request all SPID attributes. If you need just a subset of
them override the settings `SPID_REQUESTED_ATTRIBUTES` and `SPID_REQUIRED_ATTRIBUTES`.
They must be a subset of `spiddjango.SPID_ATTRIBUTES`.

# Example application

The package includes also an example that shows how to use the app. You can launch it using the command

```bash
python manage.py runsslserver --certificate example/certs/cert.pem --key example/certs/key.pem 127.0.0.1:9000
```

**NOTE: in order to use the example you will also need sslserver Django plugin**

After the example has been launched you need to configure the SP in your IdP. The metadata with all the configuration 
can be accessed at url /saml2/metadata/

The example has been tested with the AGID testenv which can be downloaded at 
https://github.com/italia/spid-testenv-docker. Refer to that project to configure the test environment. 

After the SP has been configured in the IdP go to https://localhost/ and perform the authentication selecting the AGID 
Test IdP.

# Protecting a view

Since spiddjango uses djangosaml2 and exploit its authentication backend, in order to protect a view with SPID authentication
you just need to use the `@login_required` decorator to cause the page to be redirected to the SPID authentication process.
An example is the `protected_view`, accessible at `/protected/` url.  

