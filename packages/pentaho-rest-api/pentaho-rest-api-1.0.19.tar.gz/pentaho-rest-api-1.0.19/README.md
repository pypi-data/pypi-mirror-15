# pentaho-rest-api 

[![Build Status](https://travis-ci.org/AlayaCare/pentaho-rest-api.svg?branch=master)](https://travis-ci.org/AlayaCare/pentaho-rest-api)

Python library to make call to Pentaho BA server via its REST API.
Supported Penthao BA Server is 6.0 and more.

## Version
1.0.11

## Installation

Installing the library from the pip package

```sh
$ pip install pentaho-rest-api
```

## Object Usage

Create a Pentaho object, setting its URL and its authentication type:
```
from penapi.pentaho import (
    Pentaho,
    PentahoBasicAuth
)

pentaho = Pentaho(pentaho_base_url='http://mysite.com/pentaho')

pentaho.set_auth_method(PentahoBasicAuth(username, password))

# list users
user_list = pentaho.users.list()
>>> user_list => ['admin', 'pat', 'suzy']
```

## Implemented APIS

### Users (ref: https://help.pentaho.com/Documentation/6.0/0R0/070/010/0D0/0O0)

- list users: `user_list = pentaho.users.list()`
- create user: `pentaho.users.create(username='my_user')`
- delete user: `pentaho.users.delete('my_user')` or `pentaho.users.delete(['my_user1', 'my_user2'])`
- change password: `pentaho.users.change_password('my_user', 'old_pass', 'new_pass')`

### Roles (ref: https://help.pentaho.com/Documentation/6.0/0R0/070/010/0D0/0O0)

- list roles for user: `pentaho.roles.list_for_user('test')`
- assign roles to user: `pentaho.roles.assign_to_user('test', ['power', 'business'])`
- remove roles from user: `pentaho.roles.remove_from_user('test', ['business', 'admin'])`

## Authentication Methods

Pentaho REST API supports both available methods for Pentaho authentication: **BasicAuth** and **Cookie**.

### BasicAuth

You can set BasicAuth with your username and password by using it from the library and set it to your Pentaho object.
```
from penapi.pentaho import (
    Pentaho,
    PentahoBasicAuth
)

pentaho = Pentaho(pentaho_base_url='http://mysite.com/pentaho')

pentaho.set_auth_method(PentahoBasicAuth('admin', 'password'))
```

### Cookie Authentication

If you already have a authenticated cookie for your user, you can set it to your Pentaho object like this:
```
from penapi.pentaho import (
    Pentaho,
    PentahoCookieAuth
)

pentaho = Pentaho(pentaho_base_url='http://mysite.com/pentaho')

pentaho.set_auth_method(PentahoCookieAuth('my_cookie_value'))
```

### SSL Certificate

If your Pentaho instance is with SSL but without valid certificate, you can disable certificate validation.
`pentaho.set_ssl_check(False)`

## Script Usage

If you don't want to use Pentaho object, you can directly use its functionalities via scripting:
```
import penapi

panapi.set_auth_method(PentahoBasicAuth('username', 'password'))

user_list = panapi.users.list()
```
All apis available via Pentaho object can be called via _penapi_ lib, after setting the authentication.

## License

GPL