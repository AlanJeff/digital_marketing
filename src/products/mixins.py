# for product-related

from django.http import Http404

from digitalmarket.mixins import LoginRequiredMixin

from sellers.mixins import SellerAccountMixin

class ProductManagerMixin(SellerAccountMixin, object):
	def get_object(self, *args, **kwargs):
		seller = self.get_account()
		# creating an instance of Product
		obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
		try:
			# only the related seller (who creates the product) can request the product
			obj.seller == seller
		except:
			raise Http404

		if obj.seller == seller:
			return obj
		else:
			raise Http404