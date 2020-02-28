from django.contrib import admin
from django.urls import path
from django.views import generic
from django.views.generic import TemplateView
from mortgage.models import *
from mohawk.forms import *


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import *
from django.views import View
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import os
from django.core.mail import send_mail
from django.contrib import messages
from mortgage.models import *
from datetime import *
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test


class index(TemplateView):
    template_name = 'index.html'


class CreateView(generic.CreateView):
    template_name = 'create.html'



class SignUp(View):

    def get(self, request, *args, **kwargs):
        user_form = UserCreationForm()
        profile_form = UserSignUp()
        if Organization.objects.filter(name = self.kwargs.get('org')):
            self.request.session['org'] =  self.kwargs.get('org')

        return render(request, 'signup.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'parent_organization': self.kwargs.get('org'),
        })

    def post(self, request, *args, **kwargs):
            # load both forms to check validity


        user_form = UserCreationForm(self.request.POST)
        profile_form = UserSignUp(self.request.POST)
        # if both are valid...
        if user_form.is_valid() and profile_form.is_valid():

            # save the user form and log the user in
            # saving triggers the create_user_profile function in the
            # Profile model.
            user = user_form.save(commit=False)
            # user.first_name = profile_form.cleaned_data["first_name"]
            # user.last_name = profile_form.cleaned_data["last_name"]
            user.email = user_form.cleaned_data["username"]
            user.username = user_form.cleaned_data["username"]
            user.save()
            login(request, user)

            # after having created the new row in the Profile model for the new user...
            # re-initiate the profile form with the instance and user_id
            # equal to the current user and save the form
            profile_form = UserSignUp(
                self.request.POST, instance=self.request.user.profile)
            profile = profile_form.save(commit=False)
            profile.user_type = profile_form.cleaned_data["user_type"]

            org_name = self.request.POST.get('parent_organization')
            if org_name or self.request.session.get('org'):
                if self.request.session['org']:
                    org_object = Organization.objects.get(name = self.request.session['org'])
                else:
                    org_object = Organization.objects.get(name = org_name)

                profile.parent_organization = org_object
                profile.save()
                send_mail(
                    'New User has signed up on Mohawk attached to your organization',
                    'Their name is'  + user.first_name + ' ' + user.last_name + ' signed up with the email ' + user.email + '\n Mohawk will be putting together a list of your users sign ups shortly. If you have any questions please contact the Mohawk Dev team @ sean@Mohawk.app. Thanks!  ',
                    os.environ.get('EMAIL_HOST_USER'),
                    [org_object.email],
                    fail_silently=False,
                )



            profile_form.save()
            #send email to user after signup
            send_mail(
                'Thanks for signing up with Mohawk!',
                'We at Mohawk welcome you to the Mohawk network. Mohawk is the best place to find new content and discover new content creators. If you have any questions please contact us at info@Mohawk.app.' ,
                os.environ.get('EMAIL_HOST_USER'),
                [profile.user.email],
                fail_silently=False,
            )
            #send email to admin informing of sign up
            send_mail(
                'New User has signed up on Mohawk',
                user.first_name + ' ' + user.last_name + ' signed up with the email ' + user.email,
                os.environ.get('EMAIL_HOST_USER'),
                [os.environ.get('EMAIL_HOST_USER')],
                fail_silently=False,
            )

            return redirect('/edit_profile')

        else:


            return render(request, 'signup.html', {
                'user_form': user_form,
                'profile_form': profile_form,
            })


class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = "/edit_profile/"

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            user = form.get_user()
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class Logout(FormView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")
