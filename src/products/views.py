import os

from mimetypes import guess_type 

from django.conf import settings
from wsgiref.util import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Q 
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView 

from analytics.models import TagView
from digitalmarket.mixins import (
			LoginRequiredMixin,
			MultiSlugMixin, 
			SubmitBtnMixin,
			)

from tags.models import Tag

from .mixins import ProductManagerMixin
from .models import Product 
from .forms import ProductAddForm, ProductModelForm

class ProductCreateView(LoginRequiredMixin, SubmitBtnMixin, CreateView):
	model = Product 
	template_name = "form.html"
	form_class = ProductModelForm
	# success_url = "/products/"
	submit_btn = "Add Product"

	def form_valid(self, form):
		user = self.request.user
		form.instance.user = user 
		valid_data = super(ProductCreateView, self).form_valid(form)
		form.instance.managers.add(user)
		# add all default users
		tags = form.cleaned_data.get("tags")
		if tags:
			tags_list = tags.split(",")
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(form.instance)
		return valid_data

	# Only use success_url when you want a diff redirect from
	# the "get_absolute_url" in ".models"
	
	# def get_success_url(self):
	# 	return reverse("products:list_view")
	# 	#return "/users/%s/" %(self.request.user)

class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product 
	template_name = "form.html"
	form_class = ProductModelForm
	# success_url = "/products/"
	submit_btn = "Update Product"

	def get_initial(self):
		initial = super(ProductUpdateView, self).get_initial()
		tags = self.get_object().tag_set.all()
		# Make all tags title into a list
		"""
		tag_list = []
		for x in tags:
			tag_list.append(x.title)
		"""
		initial["tags"] = ", ".join([x.title for x in tags])
		return initial

	# if this form is valid, create these tags in the database if they don't exist
	# associate these tags to the product
	def form_valid(self, form):
		valid_data = super(ProductUpdateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		obj = self.get_object()
		obj.tag_set.clear()
		if tags:
			# return a comma separated list
			tags_list = tags.split(",")
			for tag in tags_list:
				if not tag == " ":
					# creating a new Tag instance which title is based on the user-inputted tag
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					# add it to the many to many field (associate the product instance to that tag)
					new_tag.products.add(self.get_object())
		return valid_data


class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product 

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		tags = obj.tag_set.all()
		for tag in tags:
			new_view = TagView.objects.add_count(self.request.user, tag)
		return context

	# def get_object(self, *args, **kwargs):
	# 	slug = self.kwargs.get("slug")
	# 	ModelClass = self.model 
	# 	if slug is not None:
	# 		try:
	# 			obj = get_object_or_404(ModelClass, slug=slug)
	# 		except ModelClass.MultipleObjectsReturned:
	# 			obj = ModelClass.objects.filter(slug=slug).order_by("-title").first()
	# 	else:
	# 		obj = super(ProductDetailView, self).get_object(*args, **kwargs)
	# 	return obj 

class ProductDownloadView(MultiSlugMixin, DetailView):
	model = Product 

	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj in request.user.myproducts.products.all():
			filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
			# Guess the type of a file based on its filename/url
			# if missing/unknown suffix the return type will be None
			guessed_type = guess_type(filepath)[0]
			wrapper = FileWrapper(open(filepath, 'rb'))
			mimetype = 'application/force-download'
			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, content_type=mimetype)

			# display the downloaded item in attachment format
			if not request.GET.get("preview"):
				response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)
			
			response["X-SendFile"] = str(obj.media.name)
			return response 
		else:
			raise Http404


class ProductListView(ListView):
	model = Product 
	# template_name = "list_view.html"

	# def get_context_data(self, **kwargs):
	# 	context = super(ProductListView, self).get_context_data(**kwargs)
	# 	context["queryset"] = self.get_queryset()
	# 	return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(**kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs 

def create_view(request):
	# FORM
	form = ProductModelForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.sale_price = instance.price 
		instance.save() 

	# Custom form method
	# if form.is_valid():
	# 	# cleaned data returns a dictionary of POST request
	# 	data = form.cleaned_data
	# 	title = data.get("title")
	# 	description = data.get("description")
	# 	price = data.get("price")
	# 	# Create a new product
	# 	# new_obj = Product.objects.create(title=title, description=description, price=price)
	# 	new_obj = Product()
	# 	new_obj.title = title
	# 	new_obj.description = description
	# 	new_obj.price = price
	# 	new_obj.save()

	template = "form.html"
	context = {
		"form": form,
		"submit_btn": "Create Product"
	}
	return render(request, template, context)

def update_view(request, object_id=None):
	product = get_object_or_404(Product, id=object_id)
	form = ProductModelForm(request.POST or None, instance=product)
	if form.is_valid():
		instance = form.save(commit=False)
		#instance.sale_price = instance.price 
		instance.save() 
	template = "form.html"
	context = {
		"object": product,
		"form": form, 
		"submit_btn": "Update Product"
	}
	return render(request, template, context)

def detail_slug_view(request, slug=None):
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()

	template = "detail_view.html"
	context = {
		"object": product 
	}
	return render(request, template, context)

def detail_view(request, object_id=None):
	product = get_object_or_404(Product, id=object_id)
	template = "detail_view.html"
	context = {
		"object": product 
	}
	return render(request, template, context)

"""Alternative way"""
# def detail_view(request, object_id=None):
# 	if object_id is not None:
# 		try:
# 			product = Product.objects.get(id=object_id)
# 		"""
# 		when there is object id (/123/), but the id is not available
# 		--Exception
# 		"""
# 		except Product.DoesNotExist:
# 			product = None
#
# 		template = "detail_view.html"
# 		context = {
# 			"object": product 
# 		}
# 		return render(request, template, context)
# 	"""
# 	when there is no object id (/avsdv/); i.e. finding an unrelated page
# 	--Page Not Found
# 	"""
# 	else:
# 		raise Http404

	
def list_view(request):
	# list of item
	queryset = Product.objects.all()
	template = "list_view.html"
	context = {
		"queryset": queryset
	}
	return render(request, template, context)