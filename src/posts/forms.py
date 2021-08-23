from django import forms
from tinymce import TinyMCE
from .models import Post,Comment,Author
from django.contrib.auth.forms import UserChangeForm,get_user_model,UserCreationForm
User = get_user_model()
class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows':10}

        )
    )

    class Meta:
        model = Post
        fields = ('title','overview','content','thumbnail','categories','previous_post','next_post')

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea( attrs={
        'placeholder' : "Type your Comment",
        'class' : 'form-control',
        'id' : 'usercomment',
        'rows' : '4'
    })) 
    class Meta:
        model = Comment
        fields = ('content',)

        
class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',

        )
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'bio',
            'connect',
            'profile_picture',
        )  
    