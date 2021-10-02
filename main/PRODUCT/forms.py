from .models import Address
from PRODUCT import models
from django import forms

class Address_Form(forms.ModelForm):
   
   class Meta:
      model=Address
      fields='__all__'
      # excluse=('user')
