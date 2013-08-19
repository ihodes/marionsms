import os

ENVIRONMENT=os.environ.get('ENVIRONMENT', 'DEVELOPMENT')

SECRET_KEY=os.environ.get('SECRET_KEY')
HOST=os.environ.get('HOST')
HOST_NAME=os.environ.get('HOST_NAME')
PORT=int(os.environ.get('PORT'))

SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
DEBUG=os.environ.get('DEBUG', False)

del os
