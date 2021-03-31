from django.urls import path
from blogs.views import post_comment_create_and_list_view,PostDeleteView,PostUpdateView,like_unlike_post,post_comment_list_view

app_name = 'blogs'

urlpatterns = [
    path('', post_comment_list_view, name='main-post-view'),
    path('<pk>/', post_comment_create_and_list_view, name='main-detail'),
    path('Liked/',like_unlike_post,name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('<pk>/update/', PostUpdateView.as_view(), name="post-update"),
]
