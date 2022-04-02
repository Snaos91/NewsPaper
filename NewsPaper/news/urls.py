from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostList.as_view(), name='post_news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('search', PostSearch.as_view(), name='post_search'),
    path('add', PostCreateView.as_view(), name='post_add'),
]