from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('01_variables_filters', views._01_variables_filters, name='01_variables_filters'),
    path('02_tags', views._02_tags, name='02_tags'),
    path('03_layout', views._03_layout, name='03_layout'),
    path('04_static_files', views._04_static_files, name='04_static_files'),
    path('05_urls', views._05_urls, name='05_urls'),
    path('articles/<int:id>', views.articles_detail, name='articles_detail'),
    path('articles/<str:category>/<int:id>', views.articles_category, name='articles_category'),
    path('search', views.search, name='search'),
    path('06_bootstrap', views._06_bootstrap, name='06_bootstrap'),
    path('myBootstrap', views.myBootstrap, name='myBootstrap'),
]