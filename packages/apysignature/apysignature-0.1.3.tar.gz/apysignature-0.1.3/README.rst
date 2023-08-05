ApySignature
=========

Python implementation of the Ruby Signature library
(https://github.com/mloughran/signature)

Examples
--------

Client example

```python
params       = {'some'='parameters'}
token        = signature.Token('my_key', 'my_secret')
request      = signature.Request('POST', '/api/thing', params)
auth_hash    = request.sign(token)
query_params = params.update(auth_hash)

requests.post('http://myservice/api/thing', data=query_params)
```

`query_params` looks like:

```python
{
  'some'='parameters',
  'auth_timestamp'=1273231888,
  'auth_signature'='28b6bb0f242f71064916fad6ae463fe91f5adc302222dfc02c348ae1941eaf80',
  'auth_version'='1.0',
  'auth_key'='my_key'
}
```

Server example (Django)

```python
auth_request = signature.Request(request.method, str(request.path), params)
public_key = params['auth_key']
token = signature.Token(public_key, private_key)
try:
    auth_request.authenticate(token)
except AuthenticationError as e:
    return HttpResponse('Unauthorized', status=401)

  # Do whatever you need to do
end
```

Copyright
---------

Copyright (c) 2014 Erick Ponce. See LICENSE for details.
