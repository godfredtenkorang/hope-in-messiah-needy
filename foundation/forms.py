from django import forms
from .models import Payment, Comment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount", "name", "email")
        
class CommentForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter you name here...',
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here ...',
        'rows': '4',
    }))
    
    class Meta:
        model = Comment
        fields = ('username', 'content', )