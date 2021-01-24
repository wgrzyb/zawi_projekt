from owlready2 import *
class Config:
    flask_port = 5000
    flask_static_url_path = '/flask_app'


class BaseConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'do-i-really-need-this'
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY
    UPLOAD_FOLDER = './download'


class ProductionConfig(BaseConfig):
    DEVELOPMENT = False
    DEBUG = False
