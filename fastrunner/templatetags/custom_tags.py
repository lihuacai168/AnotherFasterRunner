import json
from django import template

register = template.Library()


@register.filter(name='json_dumps')
def json_dumps(value):
    try:
        return json.dumps(json.loads(value), indent=4, separators=(',', ': '), ensure_ascii=False)
    except Exception:
        return value
