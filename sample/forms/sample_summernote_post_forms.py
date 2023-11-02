from django import forms
from ..models import SampleSummernotePost

class SampleSummernotePostCreateForm(forms.ModelForm):
    
   class Meta:
       model  = SampleSummernotePost
       fields = ('post_text',)