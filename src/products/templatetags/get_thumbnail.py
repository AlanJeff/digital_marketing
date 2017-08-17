# custom template tag

from django import template

"""
To be a valid tag library, the module must contain a 
module-level variable named register that is a 
template.Library instance
"""
register = template.Library()

from ..models import Product, THUMB_CHOICES

@register.filter 
def get_thumbnail(obj, arg):
	# obj == Product instance; arg == hd//sd/micro

	"""
	Error handling
	"""
	# 'isinstance' is a built-in python module
	# if instance 'obj' is not of the class 'Product'
	arg = arg.lower()
	if not isinstance(obj, Product):
		raise TypeError("This is not a valid product model.")

	# convert THUMB_CHOICES from a tuple into a dict
	choices = dict(THUMB_CHOICES)
	if not choices.get(arg):
		raise TypeError("This is not a valid type for this model.")

	return obj.thumbnail_set.filter(type=arg).first().media.url

