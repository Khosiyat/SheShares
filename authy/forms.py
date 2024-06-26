from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authy.models import Profile

def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')

class SignupForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), label="username", max_length=30, required=True)
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input is-medium'}), label="email", max_length=100, required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), required=True, label="Confirm your password")

	class Meta:

		model = User
		fields = ('username', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
		return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-small'}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-small'}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-small'}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data

class EditProfileForm(forms.ModelForm):
	CLASS_CATEGORY = [
	('General Health', 'General Health'),
	('Mental', 'Mental'), 
	('Physical', 'Physical'),
]

	picture = forms.ImageField(required=False)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-small'}), label="first_name",max_length=50,  required=True)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-small'}), label="last_name",max_length=50,  required=True)
	location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-small'}), label="location",max_length=25,  required=True)
	githubProfile = forms.URLField(widget=forms.TextInput(attrs={'class': 'input is-small'}), label="other SM",max_length=50,  required=True, initial='instagram.com')
	linkedInnProfile = forms.URLField(widget=forms.TextInput(attrs={'class': 'input is-small'}), label="interstCategory",max_length=50,  required=True, initial='linkedin.com')
	interstCategory = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input is-small'}), choices=CLASS_CATEGORY, label="interstCategory", required=False, initial='classCategory')

	class Meta:
		model = Profile
		fields = ('picture', 'first_name', 'last_name', 'location', 'interstCategory', 'linkedInnProfile', 'githubProfile')
		