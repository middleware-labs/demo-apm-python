from django.http import JsonResponse
from django.shortcuts import render

def api_endpoint(request):
    return JsonResponse({"message": "Hello from the API!"})

def html_page(request):
    return render(request, "index.html")

def raise_exception(request):
    raise ValueError("This is a sample exception!")
