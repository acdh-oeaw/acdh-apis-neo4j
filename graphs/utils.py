import datetime
from django.apps import apps
from django.conf import settings

from apis_core.apis_metainfo.models import TempEntityClass, Uri
from webpage.utils import PROJECT_METADATA as PM

from . graph_models import NeoProject, NeoUri, NeoTempEntity


def create_project_node():
    project_node = NeoProject.create_or_update(
        {
            "neo_title": PM['title'],
            "neo_author": PM['author'],
            "neo_subtitle": PM['subtitle'],
            "neo_description": PM['description'],
        }
    )[0]
    return project_node


def create_nodes(project_node):
    print(datetime.datetime.now())
    for x in TempEntityClass.objects.all():
        try:
            ent = x.get_child_entity()
        except AttributeError:
            ent = None
        if ent is not None:
            ent_type = x.get_child_class()
            apis_uri = f"{settings.APIS_BASE_URI}{ent.get_absolute_url()}"
            my_node = NeoTempEntity.create_or_update(
                {
                    "apis_uri": apis_uri,
                    "n_name": ent.name,
                    "start_date": ent.start_date,
                    "end_date": ent.end_date,
                    "ent_type": ent_type
                }
            )[0]
            my_node.neo_project.connect(project_node)
    print(datetime.datetime.now())
    return "done"


def create_uris(project_node):
    print(datetime.datetime.now())
    for x in Uri.objects.all():
        try:
            rel_ent = x.entity.get_child_entity()
        except AttributeError:
            rel_ent = None
        if rel_ent is not None:
            my_uri = NeoUri.create_or_update(
                {
                    "uri": x.uri
                }
            )[0]
            my_uri.neo_project.connect(project_node)
            apis_uri = f"{settings.APIS_BASE_URI}{rel_ent.get_absolute_url()}"
            my_node = NeoTempEntity.create_or_update(
                {
                    "apis_uri": apis_uri,
                }
            )[0]
            my_uri.entities.connect(my_node)
        else:
            pass
    print(datetime.datetime.now())
    return "done"


def create_relations():
    print(datetime.datetime.now())
    for model in apps.get_app_config('apis_relations').get_models():
        print(model)
        for x in model.objects.all():
            try:
                source_field = getattr(x, x._meta.get_fields()[-2].name)
                rel_type = getattr(x, 'relation_type').label
                target_field = getattr(x, x._meta.get_fields()[-1].name)
            except AttributeError:
                source_field = None
                rel_type = None
                target_field = None
            if source_field is not None:
                source_url = f"{settings.APIS_BASE_URI}{source_field.get_absolute_url()}"
                target_url = f"{settings.APIS_BASE_URI}{target_field.get_absolute_url()}"
                source_node = NeoTempEntity.create_or_update(
                    {
                        "apis_uri": source_url,
                    }
                )[0]
                target_node = NeoTempEntity.create_or_update(
                    {
                        "apis_uri": target_url,
                    }
                )[0]
                rel = source_node.rel_ent.connect(
                        target_node,
                        {
                            'relation_type': rel_type
                        }
                )
    print(datetime.datetime.now())
    return "done"
