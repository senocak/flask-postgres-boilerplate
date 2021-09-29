import os
from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.getcwd(), '.env'))

app = Flask(__name__)
app.config.update({
    'ENV': os.environ.get('ENV'),
    'DEBUG': os.environ.get('DEBUG') in ['True', 'true'],
    'TESTING': os.environ.get('TESTING') in ['True', 'true'],
    'JWT_SECRET_KEY': str(os.environ.get('JWT_SECRET_KEY')),
    'JWT_BLACKLIST_ENABLED': True,
    'JWT_BLACKLIST_TOKEN_CHECKS': ['access', 'refresh'],
    'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')),
    'SQLALCHEMY_DATABASE_URI': 'postgresql://' + str(os.environ.get("DB_USERNAME")) + ':' + str(os.environ.get("DB_PASSWORD")) + '@' + str(os.environ.get("DB_HOST")) + '/' + str(os.environ.get("DB_DATABASE")),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_RECORD_QUERIES': True,
    'JSON_SORT_KEYS': False,
    'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
    'MAIL_PORT': os.environ.get('MAIL_PORT'),
    'MAIL_USE_TLS': os.environ.get('MAIL_USE_TLS') in ['True', 'true'],
    'MAIL_USE_SSL': os.environ.get('MAIL_USE_SSL') in ['True', 'true'],
    'MAIL_DEBUG': os.environ.get('DEBUG') in ['True', 'true'],
    'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'),
    'MAIL_SUPPRESS_SEND': False,
    'SWAGGER': {
        'title': os.environ.get('NAME'),
        'info': {
            'title': os.environ.get('NAME'),
            'version': os.environ.get('VERSION'),
        },
        'specs': [
            {
                'endpoint': 'swagger',
                'route': '/api/v1/swagger.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'static_url_path': '/static/swagger',
        'swagger_ui': True,
        'specs_route': '/api/v1/swagger',
        'consumes': [
            'application/x-www-form-urlencoded',
        ],
        'produces': [
            'application/json',
        ],
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'description': 'Authorization: Bearer {jwt}',
                'name': 'Authorization',
                'in': 'header',
                'scheme': 'Bearer',
                'template': 'Bearer {apiKey}'
            }
        },
        'security': [
            {
                'Bearer': []
            }
        ],
        'uiversion': 2,
        'ui_params': {
            'apisSorter': 'alpha',
            'operationsSorter': 'alpha',
        },
    }
})
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
cors = CORS(app)
fma = Marshmallow(app)
swagger = Swagger(app)
mail = Mail(app)
