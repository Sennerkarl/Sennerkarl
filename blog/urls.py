from django.urls import path # from urls from mainproject
from .import views
from .views import CommentDeleteView, CommentUpdateView, LikeView, PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), #load class PostListView as a view , and it is looking for a template with naming convention app/model_viewtype.html  this can be changed
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), #variables go in <> and it uses the primary keys of the posts
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),

    path('post/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('about/', views.about, name='blog-about'),
    path('like/<int:pk>', LikeView, name='like_post'),
]