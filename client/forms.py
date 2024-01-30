from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Documents, DocumentType

class CategoryForm(forms.Form):
    label = forms.CharField(label="Label", max_length=255, required=True)
    description = forms.CharField(label="Description", max_length=1000, widget=forms.Textarea, required=False)

class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = ['label', 'description']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['title', 'author', 'presentation_date', 'presentation_place', 'category', 'document_type']
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['presentation_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['presentation_date'].label = "Date de présentation"
        self.fields['presentation_place'].label = "Lieu de présentation"

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["last_name", "first_name", "username", "email", "password1", "password2"]