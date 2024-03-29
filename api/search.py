# Elasticsearch helpful functions
from flask import current_app


def add_to_index(index, model):
    # If not configured return
    if not current_app.elasticsearch:
        return

    # Exploit models __searchable__ variable for searching purposes
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)

    # Index the payload
    return current_app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return

    return current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch or not query:
        return [], 0  # This returned tuple needed for compatibility reasons. See below

    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        # Doing a fuzzy query that search to all searchable fields.
        body={'query': {'multi_match': {'query': query, 'type': 'most_fields', 'fields': ['*'],  "fuzziness": "AUTO"}},
              'from': (page - 1) * per_page, 'size': per_page})

    ids = [int(hit['_id']) for hit in search['hits']['hits']]

    return ids, search['hits']['total']  # Return ids with the total of hits from elastic
