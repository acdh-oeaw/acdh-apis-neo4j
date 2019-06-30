import os
from django.core.management.base import BaseCommand, CommandError

from graphs.utils import create_project_node, create_nodes, create_uris, create_relations


class Command(BaseCommand):
    # Show this when the user types help
    help = "Dumps all data into a neo4j-db"

    # A command must define handle()
    def handle(self, *args, **options):
        project_node = create_project_node()
        create_nodes(project_node)
        create_uris(project_node)
        create_relations()
        return 'done'
