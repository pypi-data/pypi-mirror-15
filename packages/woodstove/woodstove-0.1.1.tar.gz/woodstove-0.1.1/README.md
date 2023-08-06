# woodstove

[![Build Status](https://travis-ci.org/richardmarshall/woodstove.svg?branch=master)](https://travis-ci.org/richardmarshall/woodstove) [![PyPi](https://img.shields.io/pypi/v/woodstove.svg)](https://pypi.python.org/pypi/woodstove)

A simple [python](https://python.org) framework for building json http apis built ontop of the [bottle](http://bottlepy.org) microframework.

## Install

```
pip install woodstove
```

## Usage

### Example: Hello world

```python
from woodstove import app, server

class Hello(object):
    wsapp = app.App('/hello')

    @wsapp.get('/world')
    def hello_world(self):
        return "Hi!"

s = server.Server()
s.mount(Hello())
s.run(host='localhost', port=8080)
```

Run this script then point curl or your browser at http://localhost:8080/hello/world.

```
$ curl http://localhost:8080/hello/world
{"total": 1, "data": ["Hi!"]}
```

## Testing

TODO

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details on submitting patches.

## Licensing

Woodstove is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for full license text.
