#!/usr/bin/env/python2.7

from src.hextech_project_x import DB

# SQLAlchemy will generate and run SQL from all our domain objects
DB.create_all()