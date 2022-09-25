from django.urls import path
from. import views
from .views import BboardHome, PostDetailView,PostCategory,accept
from .signals import *

urlpatterns = [
    path('', BboardHome.as_view(), name='home'),#главная страница
    path('category/<slug:cat_slug>/', PostCategory.as_view(), name='category'),
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),  # Ссылка на создание новости
    path('<int:pk>/update', views.PostUpdateView.as_view(), name='post_create'),  # Ссылка на обновление новости
    path('<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),  # Ссылка на удаление новости
    path('list/', views.ListPost.as_view(), name='list_post'), # страница с откликами на  объявления пользователя
    path('accounts/profile/post/<int:pk>/', views.CommentPost.as_view(), name='comment_post'),  # фильтровать отклики по объявлениям
    path('project/comment/<int:pk>/accept/', accept,name='accept'),  # принять комментарий
    path('project/comment/<int:pk>/delete', views.DeleteComment.as_view(), name='comment_delete'),

]