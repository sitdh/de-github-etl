from email.policy import default
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, Text, Date, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

default_int = -9999
default_str = 'zzzz'

class Datetime(Base):
    __tablename__ = 'datetime'

    id = Column(BigInteger, primary_key=True)
    the_date = Column(Date)
    the_day = Column(Integer)
    the_month = Column(Integer)
    the_year = Column(Integer)
    the_time = Column(Time)
    the_hour = Column(Integer)
    the_minute = Column(Integer)
    the_second = Column(Integer)

class Organize(Base):
    __tablename__ = 'organize'

    id = Column(BigInteger, primary_key=True)
    org_id = Column(BigInteger, default=default_int)
    login = Column(String, default=default_str)
    gravatar_id = Column(String, default=default_str)
    url = Column(String, default=default_str)
    avatar_id = Column(String, default=default_str)

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, default=default_int)
    login = Column(String, default=default_str)
    node_id = Column(String, default=default_str)
    name = Column(String, default=default_str)
    avatar_url = Column(String, default=default_str)
    gravatar_id = Column(String, default=default_str)
    url = Column(String, default=default_str)
    html_url = Column(String, default=default_str)
    followers_url = Column(String, default=default_str)
    following_url = Column(String, default=default_str)
    gists_url = Column(String, default=default_str)
    starred_url = Column(String, default=default_str)
    subscriptions_url = Column(String, default=default_str)
    organizations_url = Column(String, default=default_str)
    repos_url = Column(String, default=default_str)
    events_url = Column(String, default=default_str)
    received_events_url = Column(String, default=default_str)
    user_type = Column(String, default=default_str)
    site_admin = Column(String, default=default_str)

class Repository(Base):
    __tablename__ = 'repo'

    id = Column(BigInteger, primary_key=True)
    repo_id = Column(BigInteger, default=default_str)
    node_id = Column(String, default=default_str)
    name = Column(String, default=default_str)

class Event(Base):
    __tablename__ = 'event'

    id = Column(String, primary_key=True)
    event_id = Column(String, default=default_str)
    event_type = Column(String, default=default_str)
    actor_id = Column(BigInteger, ForeignKey('user.id'), nullable=True)
    repo_id = Column(BigInteger, ForeignKey('repo.id'), nullable=True)
    org_id = Column(BigInteger, ForeignKey('organize.id'), nullable=True)

    payload = Column(Text, default=default_str)

    date_id = Column(BigInteger, default=default_int)
    created_at = Column(String)

    public = Column(Integer, default=default_int)

    repository = relationship('Repository', back_populates='event')
    user = relationship('User', back_populates='event')
    organize = relationship('Organize', back_populates='event')

    date_id = relationship('Datetime', back_populates='event')
    created_at = Column(String, nullable=True)
