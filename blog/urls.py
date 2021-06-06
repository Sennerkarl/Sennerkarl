from django.urls import path # from urls from mainproject
from .import views
from .views import AboutListView, CommentDeleteView, CommentUpdateView, LikeView, PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView, UserPostListView


urlpatterns = [
    path('', views.home, name='blog-home'), #load class PostListView as a view , and it is looking for a template with naming convention app/model_viewtype.html  this can be changed
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), #variables go in <> and it uses the primary keys of the posts
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),

    path('post/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    
    path('like/<int:pk>', LikeView, name='like_post'),

    path('archive/', views.archive, name='blog-archive'),
    path('impressum/', views.impressum, name='blog-impressum'),
    path('disclaimer/', views.disclaimer, name='blog-disclaimer'),
    path('data-privacy/', views.dataprivacy, name='blog-data-privacy'),
    path('about/', AboutListView.as_view(), name='blog-about'),
    path('coming-soon/', views.comingsoon, name='blog-coming-soon'),
    path('blog/', PostListView.as_view(), name='blog-blogs'),
    path('political-risk/', views.politicalrisk, name='blog-political-risk'),
]