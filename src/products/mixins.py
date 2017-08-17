# for product-related

from django.http import Http404

from digitalmarket.mixins import LoginRequiredMixin

class ProductManagerMixin(LoginRequiredMixin, object):
	def get_object(self, *args, **kwargs):
		user = self.request.user
		# creating an instance of Product
		obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
		try:
			# only the related user (who creates the product) can request the product
			obj.user == user
		except:
			raise Http404
		try:
			user in obj.managers.all()
		except:
			raise Http404


		if obj.user == user or user in obj.managers.all():
			return obj
		else:
			raise Http404