import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from database import Base


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    login_id = Column(String(36), nullable=True)
    profile_type = Column(String(8), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.login_id

    def get_role(self):
        return self.profile_type

    def __repr__(self):
        return '<User %r>' % self.username


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    description = Column(String(500), nullable=False)
    company = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(Integer, nullable=False)

    def get_username(self):
        return self.username

    def get_description(self):
        return self.description

    def get_company(self):
        return self.company

    def get_email(self):
        return self.email

    def get_number(self):
        return self.number
