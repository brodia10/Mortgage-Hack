from django.contrib import admin
from django.urls import path
from django.views import generic
from django.views.generic import TemplateView


from mortgage.models import *


class index(TemplateView):
    template_name = 'index.html'


class CreateView(generic.CreateView):
    template_name = 'create.html'
