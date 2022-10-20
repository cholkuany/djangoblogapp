from django import forms
from app.models import Comment, Subscribe
from django.utils.translation import gettext_lazy as _

#personal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#personal
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'content', 'email', 'name', 'website'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs["placeholder"] = "Leave a comment..."
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["name"].widget.attrs["placeholder"] = "Name"
        self.fields["website"].widget.attrs["placeholder"] = "Website (optional)"


class SubscribeForm(forms.ModelForm):
    class Meta:
        model=Subscribe
        fields='__all__'
        labels = {'email': _('')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email..."
            

# perosnal--------------->
class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'email', 'password1','password2' }
# perosnal--------------->

