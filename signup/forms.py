from django import forms
from .models import Contact, Tour
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from django.forms import ModelForm, DateTimeInput, DateInput



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('subject','message')
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('subject'),
            Field('message'),
            Submit('Submit', 'Submit', css_class="btn btn-success mt-4")
        )
        super(ContactForm, self).__init__(*args, **kwargs)


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('datefrom','dateto', 'people')
        widgets = {
            'datefrom': DateInput(attrs={'type': 'date'}),
            'dateto': DateInput(attrs={'type': 'date'}),
           
          }
        
    def __init__(self, *args, **kwargs):
        datefrom = forms.DateTimeField(required=True,input_formats=['%Y-%m-%d %H:%M'])
        dateto = forms.DateTimeField(required=True,input_formats=['%Y-%m-%d %H:%M'])

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('datefrom'),
            Field('dateto'),
            Field('people'),
            Submit('Submit', 'Submit', css_class="btn btn-success mt-4")
        )
        super(TourForm, self).__init__(*args, **kwargs)


