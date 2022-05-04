from django.conf import settings
from django.utils.module_loading import import_module
from django import template
from django.template.base import Node
from operator import itemgetter
from django.template.defaultfilters import stringfilter
from django.template import Context
from webpack_loader import utils
from webpack_loader.exceptions import WebpackBundleLookupError
from django.utils.safestring import mark_safe
import json

register = template.Library()


# @register.assignment_tag
# def to_list(*args):
# 	return args


# @register.assignment_tag
# def add_to_list(alist, add):
# 	if alist:
# 		return alist + [add]
# 	else:
# 		return [add]


@register.simple_tag
def getFeldVal(alist, val):
	if alist:
		for aDict in alist:
			if 'name' in aDict and aDict['name'] == val:
				if 'value' in aDict:
					return aDict['value']
				else:
					return
	return


@register.simple_tag(takes_context=True)
def render(context, value):
	return template.engines['django'].from_string(value).render(context)


# settings value
@register.simple_tag
def settings_value(name):
	if name in getattr(settings, 'ALLOWED_SETTINGS_IN_TEMPLATES', ''):
		return getattr(settings, name, '')
	return ''


# {{ mydict|get_item:item.NAME }}
@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)


@register.simple_tag
def render_bundle(bundle_name, extension=None, config='DEFAULT', attrs=''):
	try:
		tags = utils.get_as_tags(bundle_name, extension=extension, config=config, attrs=attrs)
	except WebpackBundleLookupError as e:
		return''
	return mark_safe('\n'.join(tags))
