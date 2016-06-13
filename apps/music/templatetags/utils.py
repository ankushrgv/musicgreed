import urllib
import urlparse

from django import template

register = template.Library()


def handle_get_params(value, arg):
	value = dict(value)
	argdict = urlparse.parse_qsl(arg)
	value.update(argdict)

	for k,v in value.iteritems():
		if isinstance(v, list):
			value[k] = v[0]

	return "?%s" % urllib.urlencode(value)	


def pageno(value):
	# print "The value is ", value
	return "page=%s" % (value)


register.filter('handle_get_params', handle_get_params)
register.filter('pageno', pageno)