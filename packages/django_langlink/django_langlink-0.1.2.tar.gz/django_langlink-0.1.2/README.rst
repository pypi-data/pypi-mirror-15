========
LangLink
========

This is a simple Django apllication that provide an abstract class to create a language model and
a management command to populate your model with language titles and their codes.

A ManyToMany relationship to this language model can be useful to define a language field on other models.

Source of the Language codes which are used in this application is: http://data.okfn.org/data/core/language-codes#resource-language-codes

Installation
============
Install the application package using pip::

    pip install django-langlink



add 'langlink' to the INSTALLED_APPS list on your settings file

How to use
==========

Import the Language abstract model from langlink and use it to create your language model::

    from langlink.models import Language

    class MyLanguageModel(Language):
        pass
    

after you create and migrate your models, run this management command to populate the data::

    python manage.py add_languages my_app_name mylanguagemodel
