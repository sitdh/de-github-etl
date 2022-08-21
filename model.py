from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, relationship, server_onupdate

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
    avatar_url = Column(String, nullable=True)
    gravatar_id = Column(String, nullable=True)
    url = Column(String, nullable=True)
    html_url = Column(String, nullable=True)
    followers_url = Column(String, nullable=True)
    following_url = Column(String, nullable=True)
    gists_url = Column(String, nullable=True)
    starred_url = Column(String, nullable=True)
    subscriptions_url = Column(String, nullable=True)
    organizations_url = Column(String, nullable=True)
    repos_url = Column(String, nullable=True)
    events_url = Column(String, nullable=True)
    received_events_url = Column(String, nullable=True)
    type = Column(String, nullable=True)
    site_admin = Column(String, nullable=True)

class Label(Base):
    __tablename__ = 'lable'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    node_id = Column(String)
    url = Column(String, nullable=True)
    name = Column(String, nullable=True)
    color = Column(String, nullable=True)
    default = Column(Boolean, nullable=True)
    description = Column(String, nullable=True)

class Repository(Base):
    __tablename__ = 'repo'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    node_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    private = Column(Boolean, nullable=True)
    html_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    fork = Column(Boolean, nullable=True)
    url = Column(String, nullable=True)
    forks_url = Column(String, nullable=True)
    keys_url = Column(String, nullable=True)
    collaborators_url = Column(String, nullable=True)
    teams_url = Column(String, nullable=True)
    hooks_url = Column(String, nullable=True)
    issue_events_url = Column(String, nullable=True)
    events_url = Column(String, nullable=True)
    assignees_url = Column(String, nullable=True)
    branches_url = Column(String, nullable=True)
    tags_url = Column(String, nullable=True)
    blobs_url = Column(String, nullable=True)
    git_tags_url = Column(String, nullable=True)
    git_refs_url = Column(String, nullable=True)

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    url = Column(String, nullable=True)
    html_url = Column(String, nullable=True)
    issue_url = Column(String, nullable=True)
    node_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    author_association = Column(String, nullable=True)
    body = Column(String, nullable=True)
    performed_via_github_app = Column(String, nullable=True)

    reaction = relationship('Reaction', back_populates='comment')

class Reaction(Base):
    __tablename__ = 'reaction'

    id = Column(BigInteger, primary_key=True)
    url = Column(String, nullable=True)
    total_count = Column(Integer, default=0)
    plus = Column(Integer, default=0)
    minus = Column(Integer, default=0)
    laugh = Column(Integer, default=0)
    hooray = Column(Integer, default=0)
    confused = Column(Integer, default=0)
    hearth = Column(Integer, default=0)
    rocket = Column(Integer, default=0)
    eyes = Column(Integer, default=0)

class Commit(Base):
    __tablename__ = 'commit'

    id = Column(String, primary_key=True)
    author = relationship('User')
    message = Column(String, nullable=True)
    distinct = Column(Boolean, default=False)
    url = Column(String, nullable=False)

class Event(Base):
    __tablename__ = 'event'

    id = Column(String, primary_key=True)
    type = Column(String, nullable=True)
    actor_id = Column(String, nullable=True)
    repo_id = Column(Boolean, default=False)
    payload_id = Column(String, nullable=False)
    public = Column(Boolean, default=True)
    created_at = Column(
        TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )