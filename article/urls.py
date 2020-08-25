from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('<slug:category>/', views.category, name="category"),
    path('<slug:category>/<slug:post>', views.singlePost , name="singlePost"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('createPost', views.createPost, name="createPost")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)