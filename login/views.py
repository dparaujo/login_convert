from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import logout
import pandas as pd

class IndexView(TemplateView):
    template_name = "index.html"

def logout_view(request):
    logout(request)
    return redirect("/")
