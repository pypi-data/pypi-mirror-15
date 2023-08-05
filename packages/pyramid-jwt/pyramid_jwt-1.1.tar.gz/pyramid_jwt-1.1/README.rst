JWT authentication for Pyramid
==============================

This package implements an authentication policy for Pyramid that using  `JSON
Web Tokens <http://jwt.io/>`_. This standard (`RFC 7519
<https://tools.ietf.org/html/rfc7519>`_) is often used to secure backens APIs.
The excellent `PyJWT <https://pyjwt.readthedocs.org/en/latest/>`_ library is
used for the JWT encoding / decoding logic.

Enabling JWT support in a Pyramid application is very simple:

.. code-block:: python

   from pyramid.config import Configurator
   from pyramid.authorization import ACLAuthorizationPolicy

   def main():
       config = Configurator()
       # Pyramid requires an authorization policy to be active.
       config.set_authorization_policy(ACLAuthorizationPolicy())
       # Enable JWT authentication.
       config.include('pyramid_jwt')
       config.set_jwt_authentication_policy('secret')

This will set a JWT authentication policy using the `Authorization` HTTP header
with a `JWT` scheme to retrieve tokens. Using another HTTP header is trivial:

.. code-block:: python

    config.set_jwt_authentication_policy('secret', http_header='X-My-Header')

To make creating valid tokens easier a new ``create_jwt_token`` method is
added to the request. You can use this in your view to create tokens. A simple
authentication view for a REST backend could look something like this:

.. code-block:: python

    @view_config('login', request_method='POST', renderer='json')
    def login(request):
        login = request.POST['login']
        password = request.POST['password']
        user_id = authenticate(login, password)  # You will need to implement this.
        if user_id:
            return {
                'result': 'ok',
                'token': request.create_jwt_token(user_id)
            }
        else:
            return {
                'result': 'error'
            }

Since JWT is typically used via HTTP headers and does not use cookies the
standard ``remember()`` and ``forget()`` functions from Pyramid are not useful.
Trying to use them while JWT authentication is enabled will result in a warning.


Extra claims
------------

Normally pyramid_jwt only makes a single JWT claim: the *subject* (or
``sub`` claim) is set to the principal. You can also add extra claims to the
token by passing keyword parameters to the ``create_jwt_token`` method.

.. code-block:: python

   token = request.create_jwt_token(user.id,
       name=user.name,
       admin=(user.role == 'admin'))


All claims found in a JWT token can be accessed through the ``jwt_claims``
dictionary property on a request. For the above example you can retrieve the
name and admin-status for the user directly from the request:

.. code-block:: python

   print('User id: %d' % request.authenticated_userid)
   print('Users name: %s', request.jwt_claims['name'])
   if request.jwt_claims['admin']:
      print('This user is an admin!')

Keep in mind that data ``jwt_claims`` only reflects the claims from a JWT
token and do not check if the user is valid: the callback configured for the
authentication policy is *not* checked. For this reason you should always use
``request.authenticated_userid`` instead of ``request.jwt_claims['sub']``.


Settings
--------

There are a number of flags that specify how tokens are created and verified.
You can either set this in your .ini-file, or pass/override them directly to the
``config.set_jwt_authentication_policy()`` function.

+--------------+-----------------+---------------+--------------------------------------------+
| Parameter    | ini-file entry  | Default       | Description                                |
+==============+=================+===============+============================================+
| private_key  | jwt.private_key |               | Key used to hash or sign tokens.           |
+--------------+-----------------+---------------+--------------------------------------------+
| public_key   | jwt.public_key  |               | Key used to verify token signatures. Only  |
|              |                 |               | used with assymetric algorithms.           |
+--------------+-----------------+---------------+--------------------------------------------+
| algorithm    | jwt.algorithm   | HS512         | Hash or encryption algorithm               |
+--------------+-----------------+---------------+--------------------------------------------+
| expiration   | jwt.expiration  |               | Number of seconds (or a datetime.timedelta |
|              |                 |               | instance) before a token expires.          |
+--------------+-----------------+---------------+--------------------------------------------+
| leeway       | jwt.leeway      | 0             | Number of seconds a token is allowed to be |
|              |                 |               | expired before it is rejected.             |
+--------------+-----------------+---------------+--------------------------------------------+
| http_header  | jwt.http_header | Authorization | HTTP header used for tokens                |
+--------------+-----------------+---------------+--------------------------------------------+
| auth_type    | jwt.auth_type   | JWT           | Authentication type used in Authorization  |
|              |                 |               | header. Unused for other HTTP headers.     |
+--------------+-----------------+---------------+--------------------------------------------+
