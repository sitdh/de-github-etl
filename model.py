from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Organize(Base):
    __tablename__ = 'organize'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    login = Column(String)
    gravatar_id = Column(String)
    url = Column(String)
    avatar_id = Column(String)

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    login = Column(String)
    node_id = Column(String)
    name = Column(String, nullable=True)
    avatar_url = Column(String)
    gravatar_id = Column(String)
    url = Column(String)
    html_url = Column(String)
    followers_url = Column(String)
    following_url = Column(String)
    gists_url = Column(String)
    starred_url = Column(String)
    subscriptions_url = Column(String)
    organizations_url = Column(String)
    repos_url = Column(String)
    events_url = Column(String)
    received_events_url = Column(String)
    type = Column(String)
    site_admin = Column(String)

class Label(Base):
    __tablename__ = 'lable'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    node_id = Column(String)
    url = Column(String)
    name = Column(String)
    color = Column(String)
    default = Column(Boolean)
    description = Column(String, nullable=True)

class Repository(Base):
    __tablename__ = 'repo'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String)
    url = Column(String)

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    url = Column(String)
    html_url = Column(String)
    issue_url = Column(String)
    node_id = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    author_association = Column(String)
    body = Column(String)
    reaction = relationship('Reaction', back_populates='comment')
    performed_via_github_app = Column(String, nullable=True)

class Reaction(Base):
    __tablename__ = 'reaction'

    id = Column(BigInteger, primary_key=True)
    url = Column(String)
    total_count = Column(Integer)
    plus = Column(Integer)
    minus = Column(Integer)
    laugh = Column(Integer)
    hooray = Column(Integer)
    confused = Column(Integer)
    hearth = Column(Integer)
    rocket = Column(Integer)
    eyes = Column(Integer)

    comment = relationship('Comment', back_populates=('reaction'))