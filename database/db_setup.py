# db_setup.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

def load_environment():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dotenv_path = os.path.join(project_root, '.env')
    load_dotenv(dotenv_path)
    database_uri = os.getenv("DATABASE_URL")
    if not database_uri:
        raise ValueError("No DATABASE_URL found in the environment variables.")
    return database_uri

def create_database_engine(uri):
    return create_engine(uri, connect_args={"options": "-c password_encryption=scram-sha-256"})

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def main():
    uri = load_environment()
    engine = create_database_engine(uri)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")

if __name__ == '__main__':
    main()
