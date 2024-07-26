import os

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
	UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship, One, OneOrMore,
    DateTimeProperty)
from neomodel.properties import JSONProperty
from neomodel import db

from neomodel import config
from neo4j import GraphDatabase

neo4j_url = os.getenv("NEO4J_URL")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

config.DATABASE_URL = f"bolt://{neo4j_username}:{neo4j_password}@{neo4j_url}"
config.DRIVER = GraphDatabase.driver(f"bolt://{neo4j_url}")

class MindwmUser(StructuredNode):
    username = StringProperty(required = True)
    host = RelationshipTo('MindwmHost', 'HAS_MINDWM_HOST')
    atime = DateTimeProperty(default_now = True)

class MindwmHost(StructuredNode):
    hostname = StringProperty(required = True)
    tmux = RelationshipTo('Tmux', 'HAS_TMUX', cardinality=OneOrMore)
    clipboard = RelationshipTo('ClipBoard', 'HAS_CLIPBOARD', cardinality=OneOrMore)
    atime = DateTimeProperty(default_now = True)

class Tmux(StructuredNode):
    socket_path = StringProperty(required = True)
    host_id = IntegerProperty(required = True)
    host = RelationshipFrom('MindwmHost', 'HAS_TMUX', cardinality=One)
    session = RelationshipTo('TmuxSession', 'HAS_TMUX_SESSION', cardinality=OneOrMore)
    atime = DateTimeProperty(default_now = True)

class TmuxSession(StructuredNode):
    name = StringProperty(required = True)
    tmux_id = IntegerProperty(required = True)
    socket_path = RelationshipFrom('Tmux', 'HAS_TMUX', cardinality=One)
    pane = RelationshipTo('TmuxPane', 'HAS_TMUX_PANE', cardinality=OneOrMore)
    atime = DateTimeProperty(default_now = True)

class TmuxPane(StructuredNode):
    pane_id = IntegerProperty(required = True)
    session_id = IntegerProperty(required = True)
    session = RelationshipFrom('TmuxSession', 'HAS_TMUX_PANE', cardinality=One)
    title = StringProperty()
    contextParameters = JSONProperty(default={})
    io_document = Relationship('IoDocument', 'HAS_IO_DOCUMENT')
    atime = DateTimeProperty(default_now = True)

class IoDocument(StructuredNode):
    uuid = StringProperty(unique_index=True, required = True)
    user_input = StringProperty(required = True)
    output = StringProperty(required = True)
    ps1 = StringProperty(required = True)
    time = DateTimeProperty(default_now = True)
    tmux_pane = Relationship('TmuxPane', 'HAS_IO_DOCUMENT')
    atime = DateTimeProperty(default_now = True)
    
class ClipBoard(StructuredNode):
    uuid = StringProperty(unique_index=True, required = True)
    time = DateTimeProperty(default_now = True)
    data = StringProperty(required = True)
    host = RelationshipFrom('MindwmHost', 'HAS_CLIPBOARD', cardinality=One)
    atime = DateTimeProperty(default_now = True)
