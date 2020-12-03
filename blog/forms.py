from logging import PlaceHolder
from .models import Post, Comment
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, ButtonHolder, Div, Field
from crispy_forms.bootstrap import PrependedText

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False
        self.helper.field_class = ''
        self.helper.layout = Layout(
            Field(PrependedText('content','Add Comment', placeholder='Your comment right here'))
        )
        
        
        
       
        
        
        

    