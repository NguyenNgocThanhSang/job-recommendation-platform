from django import forms

class SignUpForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField()
  username = forms.CharField()

class SignInForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField()

class ForgotPasswordForm(forms.Form):
  email = forms.EmailField()

class GetJobsForm(forms.Form):
  page = forms.IntegerField(required=False)

class ChatBotForm(forms.Form):
  job_id = forms.IntegerField()
  message = forms.CharField()