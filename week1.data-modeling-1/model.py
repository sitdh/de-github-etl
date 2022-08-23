from email.policy import default
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, Text, Date, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

default_int = -9999
default_str = 'zzzz'

class Datetime(Base):
    __tablename__ = 'datetime'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    the_datetime = Column(TIMESTAMP, nullable=True)
    the_datetime_str = Column(String, nullable=True)
    the_date = Column(Date, nullable=True)
    the_day = Column(Integer, default=default_int)
    the_month = Column(Integer, default=default_int)
    the_year = Column(Integer, default=default_int)
    the_time = Column(Time, nullable=True)
    the_hour = Column(Integer, default=default_int)
    the_minute = Column(Integer, default=default_int)
    the_second = Column(Integer, default=default_int)

    events = relationship('Event')

class Organize(Base):
    __tablename__ = 'organize'

    id = Column(BigInteger, primary_key=True)
    org_id = Column(BigInteger, default=default_int)
    login = Column(String, default=default_str)
    gravatar_id = Column(String, default=default_str)
    url = Column(String, default=default_str)
    avatar_id = Column(String, default=default_str)

    events = relationship('Event')

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, default=default_int)
    login = Column(String, default=default_str)
    display_login = Column(String, default=default_str)
    gravatar_id = Column(String, default=default_str)
    url = Column(String, default=default_str)
    avatar_id = Column(String, default=default_str)

    events = relationship('Event')

class Repository(Base):
    __tablename__ = 'repo'

    id = Column(BigInteger, primary_key=True)
    repo_id = Column(BigInteger, default=default_str)
    name = Column(String, default=default_str)
    url = Column(String, default=default_str)

    events = relationship('Event')

class Event(Base):
    __tablename__ = 'event'

    id = Column(String, primary_key=True)
    event_id = Column(String, default=default_str)
    event_type = Column(String, default=default_str)
    actor_id = Column(BigInteger, ForeignKey('user.id'), nullable=True)
    repo_id = Column(BigInteger, ForeignKey('repo.id'), nullable=True)
    org_id = Column(BigInteger, ForeignKey('organize.id'), nullable=True)

    payload = Column(Text, default=default_str)
    created_at = Column(String, nullable=True)
    public = Column(Integer, default=default_int)
    date_id = Column(BigInteger, ForeignKey('datetime.id'))

    repository = relationship('Repository', back_populates='events')
    user = relationship('User', back_populates='events')
    organize = relationship('Organize', back_populates='events')

    datetime_data = relationship('Datetime', back_populates='events')
