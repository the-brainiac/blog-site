from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


app_name='blogs'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='detail'),
    path('blog/create', views.BlogCreateView.as_view(success_url=reverse_lazy('blogs:all')), name='create'),
    path('blog/<int:pk>/update', views.BlogUpdateView.as_view(success_url=reverse_lazy('blogs:all')), name='update'),
    path('blog/<int:pk>/delete', views.BlogDeleteView.as_view(success_url=reverse_lazy('blogs:all')), name='delete'),

    path('blog/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='comment_delete'),


    path('blog/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='favorite'),
    path('blog/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='unfavorite'),

    
]