runwsgi
===============
A simple runner for Python wsgi application. Like Gunicorn but can run on Windows. It's to simple, so **do not use at production environment**.

Install
===============
::

 pip install runwsgi


Use
===============
run command:

::

 runwsgi -b 128.0.0.1:8000 -d /home/robin/demo/ -p "robin" demo:app

on Windows use:
::

 runwsgi.bat -b 128.0.0.1:8000 -d C:\Users\Administrator\Desktop\demo\ -p "robin" demo:app

if can't find runwsgi command, try:
::

 python -m runwsgi -b 128.0.0.1:8000 -d /home/robin/demo/ -p "robin" demo:app


open broswer with url **http://127.0.0.1:8000**
	

Other tips
===============
1. -b
::

 set bind address

2. -d
::

 set you wsgi work dir

3. -p
::

 set environment variable of WSGI_PARAMS, and then you can use "os.environ.get('WSGI_PARAMS')" to get the parameter.

4. wsgi application
::

 model:application
