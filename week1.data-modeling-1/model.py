from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, relationship, server_onupdate

Base = declarative_base()

default_int = -9999
default_str = 'zzzz'

class Datetime(Base):
    __tablename__ = 'dim_datetime'

    id = Column(BigInteger, primary_key=True)
    # org_id = Column(BigInteger, default=default_int)
    # login = Column(String, default=default_str)
    # gravatar_id = Column(String, default=default_str)
    # url = Column(String, default=default_str)
    # avatar_id = Column(String, default=default_str)

class Organize(Base):
    __tablename__ = 'dim_organize'

    id = Column(BigInteger, primary_key=True)
    org_id = Column(BigInteger, default=default_int)
    login = Column(String, default=default_str)
    gravatar_id = Column(String, default=default_str)
    url = Column(String, default=default_str)
    avatar_id = Column(String, default=default_str)

class User(Base):
    __tablename__ = 'dim_user'

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
    type = Column(String, default=default_str)
    site_admin = Column(String, default=default_str)

class Label(Base):
    __tablename__ = 'dim_label'

    id = Column(BigInteger, primary_key=True)
    label_id = Column(BigInteger, default=default_int)
    node_id = Column(String, default=default_str)
    url = Column(String, default=default_str)
    name = Column(String, default=default_str)
    color = Column(String, default=default_str)
    default_value = Column(Integer, default=default_int)
    description = Column(String, default=default_str)

class Repository(Base):
    __tablename__ = 'dim_repo'

    id = Column(BigInteger, primary_key=True)
    repo_id = Column(BigInteger, default=default_str)
    node_id = Column(String, default=default_str)
    name = Column(String, default=default_str)
    full_name = Column(String, default=default_str)
    private = Column(Integer, default=default_int)
    html_url = Column(String, default=default_str)
    description = Column(String, default=default_str)
    fork = Column(Integer, default=default_int)
    url = Column(String, default=default_str)
    forks_url = Column(String, default=default_str)
    keys_url = Column(String, default=default_str)
    collaborators_url = Column(String, default=default_str)
    teams_url = Column(String, default=default_str)
    hooks_url = Column(String, default=default_str)
    issue_events_url = Column(String, default=default_str)
    events_url = Column(String, default=default_str)
    assignees_url = Column(String, default=default_str)
    branches_url = Column(String, default=default_str)
    tags_url = Column(String, default=default_str)
    blobs_url = Column(String, default=default_str)
    git_tags_url = Column(String, default=default_str)
    git_refs_url = Column(String, default=default_str)

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BigInteger, primary_key=True)
    comment_id = Column(BigInteger, nullable=True)
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
    __tablename__ = 'dim_reaction'

    id = Column(BigInteger, primary_key=True)
    reaction_id = Column(BigInteger, default=default_int)
    url = Column(String, default=default_str)
    total_count = Column(Integer, default=default_int)
    plus = Column(Integer, default=default_int)
    minus = Column(Integer, default=default_int)
    laugh = Column(Integer, default=default_int)
    hooray = Column(Integer, default=default_int)
    confused = Column(Integer, default=default_int)
    hearth = Column(Integer, default=default_int)
    rocket = Column(Integer, default=default_int)
    eyes = Column(Integer, default=default_int)

class Commit(Base):
    __tablename__ = 'dim_commit'

    id = Column(BigInteger, primary_key=True)
    id = Column(String, default=default_str)
    message = Column(String, default=default_str)
    distinct = Column(Integer, default=default_int)
    url = Column(String, default=default_str)

class Event(Base):
    __tablename__ = 'fact_event'

    id = Column(String, primary_key=True)
    event_id = Column(String, nullable=True)
    type = Column(String, nullable=True)
    actor_id = Column(String, nullable=True)
    repo_id = Column(Boolean, default=False)
    payload_id = Column(String, nullable=False)
    public = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )