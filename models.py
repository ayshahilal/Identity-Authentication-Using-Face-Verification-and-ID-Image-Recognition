from sqlalchemy import Column, String, Integer, Boolean, create_engine, Date
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False)
    password = Column(String(128), nullable=False)
    token = Column(String(128))
    is_verified = Column(Boolean, nullable=True, default=False)

    firstname = Column(String(32))
    lastname = Column(String(32))
    email = Column(String(32))
    tc = Column(String(32))
    birth_date = Column(Date)
    gender = Column(Boolean)

    def __repr__(self):
        return repr({'id': self.id, 'name': self.name, 'email': self.email})

if __name__ == "__main__":
    DATABASE_URL = os.getenv('DATABASE_URL')
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)