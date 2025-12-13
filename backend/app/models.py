from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)


class Sweet(Base):
    __tablename__ = "sweets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
