"""bookmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r"^login/$", views.Login.as_view()),

    re_path(r"^(publisher|book|author)_del/(\d+)", views.Delete.as_view(), name="del"),

    # path('publisher_list/', views.publisher_list),
    path('publisher_list/', views.PublisherList.as_view(), name="publisher"),
    # path('publisher_add/', views.publisher_add),
    path('publisher_add/', views.PublisherAdd.as_view(), name="pub_add"),
    # path('publisher_del/', views.publisher_del),
    # path('publisher_del/', views.PublisherDel.as_view()),
    # re_path(r'^publisher_del/(?P<pk>\d+)/$', views.PublisherDel.as_view()),
    # path('publisher_edit/', views.publisher_edit),
    re_path(r'^publisher_edit/(?P<pk>\d+)/$', views.PublisherEdit.as_view(), name="pub_edit"),

    # path('book_list/', views.book_list),
    path('book_list/', views.BookList.as_view(), name="book"),
    # path('book_add/', views.book_add),
    path('book_add/', views.BookAdd.as_view(), name="bk_add"),
    # path('book_del/', views.book_del),
    # path('book_del/', views.BookDel.as_view()),
    # path('book_edit/', views.book_edit),
    re_path(r'^book_edit/(?P<book_id>\d+)/$', views.BookEdit.as_view(), name="bk_edit"),

    # path('author_list/', views.author_list),
    path('author_list/', views.AuthorList.as_view(), name="author"),
    # path('author_add/', views.author_add),
    path('author_add/', views.AuthorAdd.as_view(), name="auh_add"),
    # path('author_del/', views.author_del),
    # path('author_del/', views.AuthorDel.as_view()),
    # path('author_edit/', views.author_edit),
    re_path(r'^author_edit/(?P<author_id>\d+)/$', views.AuthorEdit.as_view(), name="auh_edit"),

    path('templates_test/', views.templates_test),
    path('get_json/', views.get_json),

]
