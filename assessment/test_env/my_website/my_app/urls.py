from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from my_app.views import Comment_view

urlpatterns = [
    path('',views.home,name="home"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout,name="logout"),
    path('index/',views.index,name="index"),
    path('upload/',views.upload_view,name="upload"),
    path('like-post/<str:id>', views.like_post, name='like-post'),
    path('comment_view/', views.Comment_view, name='comment_view'),
    path('#<str:id>', views.home_post),
    path('follow', views.follow, name='follow'),
    path('profile/<str:username>/', views.profile,name='profile'),
    

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
