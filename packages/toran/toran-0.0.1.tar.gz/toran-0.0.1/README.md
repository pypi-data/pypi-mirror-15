# The Toran WSGI module
This is an API gateway built on top of python's native wsgiref module. It aims to be as
simplistic and configurable as possible without recompiling the source.

## Config Driven Development
The gateway was built with one thing in mind: ''Write less code, Write more config files''. Why? Because you would
prefer to have modular, understandable elements in a key element of the architecture.

### actions.ini
In here you can create/update/delete different actions to take on any resource. For example a list is a GET on a 
resource without ID specified while a delete is a DELETE method with id specified.

### rules.ini
In here you provide the rules for each resource, what actions they can perform (list, create,
etc).

## The Server Script
***server.py*** is a python script that loads the config files once and starts serving requests using wsgi. Please
check out the handlers package and its utils.

## Reloading
There is a script called *reloader.py* that changes a byte in a file which then is kept in memory by the server, 
the server then checks it and reloads the configs without missing requests (This happens on the single next request).
