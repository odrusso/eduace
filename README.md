![Image](https://github.com/odrusso/eduace/blob/master/docs/resources/logo_small.png)

![Python3.7](https://img.shields.io/badge/python-3.7-brightgreen.svg) ![SymPy1.2](https://img.shields.io/badge/SymPy-1.2-brightgreen.svg) ![Flask](https://img.shields.io/badge/flask-1.0.2-brightgreen.svg)

Eduace NZ development, repository, and (some) documentation

# Installation

`pip3 install -r requirements.txt` will install all dependencies for the project. It is reccomended that you use a Python Virtual Enviroment or a doker instance to minimise conflicts. 

A `config.py` file will need to be created with the addresses of the databases, secret keys, and other sensitive variables. 

# To use
`python3 app.py` will launch the Flask development server.

# To deploy
It is reccomended to run the Flask application within a Gunicorn instance (inside a Virtual Enviroment), that is reverse-proxied through an Nginx or Apache webserver for security. A hypervisor such as "Supervisor" is reccomended for realtime analytics. 
