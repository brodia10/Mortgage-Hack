from django import forms
from mortgage.models import *
# from mortgage.model_lists import *
# from mohawk.helper_functions import *



class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        help_text='100 characters max.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }))

    from_email = forms.EmailField(
        help_text='100 characters max.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }))

    subject = forms.CharField(
        max_length=100,
        help_text='100 characters max.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }))

    contact_message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control message',
                'rows': 5,
                'cols': 40,
            }))


class UserSignUp(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			"email",
			"user_type",
		]
		# widgets = {
		# 	'user_type':forms.RadioSelect(),
		# }

	def __init__(self, *args, **kwargs):
		super(UserSignUp, self).__init__(*args, **kwargs)
