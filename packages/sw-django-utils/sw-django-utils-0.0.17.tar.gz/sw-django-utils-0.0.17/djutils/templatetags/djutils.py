# coding: utf-8
import json

from django import template
import sqlparse

register = template.Library()


@register.filter('pretty_sql')
def pretty_sql(sql):
    try:
        sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        return sql
    except Exception:
        return sql


@register.filter('pretty_json')
def pretty_json(json_text):
    try:
        pretty_json_text = json.dumps(json_text, indent=4)
        return pretty_json_text
    except Exception:
        return json_text


@register.filter('from')
def get_value_from_dict(dict, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    return dict.get(key)

