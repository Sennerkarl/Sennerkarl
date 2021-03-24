from .models import Post
from users.forms import EmailSignupForm

Posts = Post.objects.all()[:5]


def grabpost(*args):
    return {'Posts':Posts}

def subscribeform(*args):
    form = EmailSignupForm()
    context = {'subscribeform':form}
    return context


