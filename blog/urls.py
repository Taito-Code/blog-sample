from django.urls import path
from . import views

urlpatterns = [
  path("", views.index.as_view(), name="index"),
  path("new/",views.new, name="new"),
  path("article/all/", views.article_all, name="article_all"),
  path("article/<int:pk>/", views.view_article, name="view_article"),
  path("article/<int:pk>/edit/", views.edit, name="edit"),
  path("article/<int:pk>/delete/",views.delete,name="delete"),
  path('article/<int:pk>/ine_ajax/', views.add_ine, name='ine'),
]