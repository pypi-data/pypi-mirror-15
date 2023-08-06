==============================
django-easyconfig |nlshield|
==============================


This app will make it easy to customize external Django apps 
that use it.

It takes an approach very similar to the old django.contrib.comments 
(now django-comments) framework. It makes it easy to use custom 
forms, values, etc.

Quick example...

Say you have an open source Django app that lets you upload a 
Photo and some metadata to that photo. To be able to customize 
that form, the project owners would have to hack the app's 
source to fit their needs (class names, etc.) or you have to 
make your app customizable. That's where django-easyconfig 
comes in...


Install
-------

Basic Install:

  $ python setup.py build
  $ sudo python setup.py install

Alternative Install (Manually):

Place webutils directory in your Python path. Either in your Python 
installs site-packages directory or set your $PYTHONPATH environment 
variable to include a directory where the webutils directory lives.


Use
---

* XXX * These are not great docs. I'll work on updating this soon!

You must create a "Config" object in your app and use that to fetch 
any object or value you want to be able to have customized.

Here is a basic example.

### yourapp/config.py
::

    from easyconfig import EasyConfig
    from django.contrib.auth.forms import AuthenticationForm
    from yourapp.forms import PasswordChangeForm


    class Config(object):
        ''' Base config class to easily pass forms, etc. to 
            yourapp views.
        '''
        # Use the dotted Python path to this class
        config = EasyConfig('yourapp.config.Config', 'YOURAPP_CONFIG')
	
        def get_login_form(self):
            return self.config.get_object('get_login_form', AuthenticationForm)

        def get_password_change_form(self):
            return self.config.get_object('get_password_change_form', PasswordChangeForm)


Now, you just need to use your yourapp.Config class any time you need 
to fetch one of these objects for use.

Here's how it could be used in a urls.py file

### urls.py
::

    from django.conf.urls import url
    from yourapp import views
    from yourapp.config import Config


    config = Config()

    urlpatterns = [
        url(r'^login/$',
            views.login, {
                'template_name': 'yourapp/login.html',
                'authentication_form': config.get_login_form(),
            }, name='yourapp-login'),
        url(r'^passwd_change/$',
            views.passwd_change, {
                'template_name': 'yourapp/passwd_change.html',
                'passwd_change_form': config.get_password_change_form(),
            }, name='yourapp-passwd-change'),
    ]

Now, anybody using your app in their own project can easily change the 
login and password change forms to whatever form they want. Here is how
they would do so in their own project.


### settings.py
::

    # Dotted python path to their own CustomConfig class
    YOURAPP_CONFIG = 'myproject.myapp.config.CustomConfig'

### myproject/myapp/config.py
::

    from myproject.myapp.forms import AuthForm, ChangeForm


    class CustomConfig(object):    
        ''' Customize the forms!
        '''
        def get_login_form(self):
            return AuthForm
    
        def get_password_change_form(self):
            return ChangeForm


That's it. Easy right? :)


Copyright & Warranty
--------------------
All documentation, libraries, and sample code are 
Copyright 2010 Peter Sanchez <petersanchez@gmail.com>. The library and 
sample code are made available to you under the terms of the BSD license 
which is contained in the included file, BSD-LICENSE.

==================
Commercial Support
==================
This software, and lots of other software like it, has been built in 
support of many of Netlandish's own projects, and the projects of our 
clients. We would love to help you on your next project so get in 
touch by dropping us a note at hello@netlandish.com.


.. |nlshield| image:: https://img.shields.io/badge/100%-Netlandish-blue.svg?style=square-flat
              :target: http://www.netlandish.com

