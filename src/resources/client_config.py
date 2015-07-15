# Run in debug mode for useful error messages
DEBUG = True

# DB config - FWIW I don't like this being here since it's exposed to the templating
# engine and could thus accidentally end up being printed to the client, but apparently
# Flask-SQLAlchemy expects this config to be defined...
SQLALCHEMY_DATABASE_URI = "mysql://root:fake@localhost/hextechprojectx"