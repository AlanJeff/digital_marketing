import datetime

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render




class CheckoutTestView(View):

	def post(self, request, *args, **kwargs):
		print(request.POST.get("testData"))
		if request.is_ajax():
			data = {
				"works": True,
				"time": datetime.datetime.now()
			}
			return JsonResponse(data)
		return HttpResponse("hello there")

	def get(self, request, *args, **kwargs):
		template = "checkout/test.html"
		context = {}
		return render(request, template, context)