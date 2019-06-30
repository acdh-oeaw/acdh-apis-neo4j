# acdh-apis-neo4j

a django app for serializing data from APIS-projects to neo4j

`pip install neomodel`

add `graphs` to `INSTALLED_APPS`

provide a NEO4J settings dict in your (secret) settings file, e.g.

```
NEO4J = {
    "NEO4J_BOLT_URL": "bolt://USER:PW@localhost:7687"
}
```

run `python manage.py to_neo4j` to dump your data to neo4j
