from django.conf import settings

from neomodel import (
    config, StructuredNode, StringProperty,
    DateProperty, Relationship, StructuredRel
)

from webpage.utils import PROJECT_METADATA

config.DATABASE_URL = settings.NEO4J.get('NEO4J_BOLT_URL', None)


class NeoTempEntRel(StructuredRel):
    start_date = DateProperty()
    start_date_written = StringProperty()
    end_date = DateProperty()
    end_date_written = StringProperty()
    relation_type = StringProperty()


class NeoTempEntity(StructuredNode):
    apis_uri = StringProperty(unique_index=True, required=True)
    n_name = StringProperty(unique=False)
    start_date = DateProperty()
    start_date_written = StringProperty()
    end_date = DateProperty()
    end_date_written = StringProperty()
    ent_type = StringProperty()
    rel_ent = Relationship('NeoTempEntity', 'RELATED', model=NeoTempEntRel)
    neo_project = Relationship('NeoProject', 'RELATED_PROJECT')

    def __str__(self):
        return f"{self.n_name}"


class NeoProject(StructuredNode):
    neo_title = StringProperty(unique_index=True, required=True)
    neo_author = StringProperty()
    neo_subtitle = StringProperty()
    neo_description = StringProperty()
    neo_public = StringProperty()


class NeoUri(StructuredNode):
    uri = StringProperty(unique_index=True, required=True)
    entities = Relationship('NeoTempEntity', 'IDENTIFIES')
    neo_project = Relationship('NeoProject', 'RELATED_PROJECT')
