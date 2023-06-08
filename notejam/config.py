import os
import urllib.parse 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
connection_string = os.getenv('SQLCONNSTR_AZURE_APP_CONFIG_CONNECTION_STRING')
params = urllib.parse.quote_plus(connection_string)

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'notejam-flask-secret-key'
    WTF_CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'notejam-flask-secret-key'
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True	

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'notejam.db')
    #SQLALCHEMY_DATABASE_URI = 'sqlite://'
class TestingConfig(Config):
    TESTING = True
    """
    Tests will run WAY faster using in memory SQLITE database
    See: https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#connect-strings
    """
    #SQLALCHEMY_DATABASE_URI = 'sqlite://'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'notejam.db')
