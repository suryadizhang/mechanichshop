from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Initialize extensions without app context
# These will be bound to the app in the create_app() function
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()