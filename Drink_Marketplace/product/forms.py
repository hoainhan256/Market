from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Viết bình luận của bạn...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
