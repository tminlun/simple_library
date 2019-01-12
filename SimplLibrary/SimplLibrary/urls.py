"""SimplLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Book.views import IndexView, AddBookView, DeleteBookView,ModificationBookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('add_book/', AddBookView.as_view(), name="add_book"),#添加图书"
    path('delete_book/', DeleteBookView.as_view(), name="delete_book"),#添加图书"
    path('modification_book/', ModificationBookView.as_view(), name="modification_book"),#添加图书"
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)