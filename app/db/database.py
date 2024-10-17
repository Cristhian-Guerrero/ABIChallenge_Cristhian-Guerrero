import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Revisar si estamos en el entorno de test
TESTING = os.getenv('TESTING', 'False') == 'True'

if TESTING:
    DATABASE_URL = 'sqlite:///./test.db'
else:
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/predictions_db')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if TESTING else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
