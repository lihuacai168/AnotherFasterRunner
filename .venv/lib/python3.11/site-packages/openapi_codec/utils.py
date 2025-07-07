def link_sorting_key(link_item):
    keys, link = link_item
    action_priority = {
        '': 0, 'get': 0,
        'post': 1,
        'put': 2,
        'patch': 3,
        'delete': 4
    }.get(link.action, 5)
    return (link.url, action_priority)


def get_links_from_document(node, keys=()):
    links = []
    for key, link in getattr(node, 'links', {}).items():
        # Get all the resources at this level
        index = keys + (key,)
        links.append((index, link))
    for key, child in getattr(node, 'data', {}).items():
        # Descend into any nested structures.
        index = keys + (key,)
        links.extend(get_links_from_document(child, index))
    return sorted(links, key=link_sorting_key)


def get_method(link):
    method = link.action.lower()
    if not method:
        method = 'get'
    return method


def get_encoding(link):
    encoding = link.encoding
    has_body = any([get_location(link, field) in ('form', 'body') for field in link.fields])
    if not encoding and has_body:
        encoding = 'application/json'
    elif encoding and not has_body:
        encoding = ''
    return encoding


def get_location(link, field):
    location = field.location
    if not location:
        if get_method(link) in ('get', 'delete'):
            location = 'query'
        else:
            location = 'form'
    return location
