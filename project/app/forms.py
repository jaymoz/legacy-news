from django import forms
from tinymce.widgets import TinyMCE
from .models import *

class PaymentDetailForm(forms.Form):
	email = forms.CharField(widget=forms.TextInput(attrs={"name":"email","type":"email", "id":"email-address", "placeholder":"Email Address"}), required=True)
	amount = forms.CharField()

class TinyMCEWidget(TinyMCE):
	def use_required_attribute(self, *args):
		return False

class PostForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCEWidget(attrs={'cols':30,'rows':10,}), required=False)

	class Meta:
		model = Post
		fields = ('title','overview','content','thumbnail','categories','featured','previous_post','next_post','video')

class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'form-control',
		'placeholder': 'Type your comment',
		'id': 'usercomment',
		'rows': '4'
	}))
	class Meta:
		model = Comment
		fields = ('content', )

class ContactForm(forms.Form):
	name = forms.CharField(required=False)
	email = forms.EmailField(required=True)
	message = forms.CharField(required=True)


#
# class DonationForm(forms.ModelForm):
# 	first_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text','id':'first-name','placeholder':'First Name'}), required=False)
# 	last_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text','id':'last-name','placeholder':'Last Name'}),required=False)
# 	amount = forms.CharField(widget=forms.TextInput(attrs={'type':'tel','id':'amount','placeholder':'Amount(₦)'}),required=True)
# 	email = forms.EmailField(widget=forms.TextInput(attrs={'type':'email','id':'email-address','placeholder':'Email Address'}),required=True)
