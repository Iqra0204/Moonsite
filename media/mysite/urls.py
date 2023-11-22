"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .import views
urlpatterns = [
path('admin/', admin.site.urls),
path('base/',views.base,name='base'),
path('',views.home,name='home'),
path('aboutus',views.aboutus,name='aboutus'),
path('contact',views.contact,name='contact'),
path('accounts/login',views.loginpage,name='login'),
path("logout",views.logoutpage,name='logout'),
path('accounts/register',views.register,name='register'),
path('courses',views.course,name='course'),
path('search/courses',views.search_courses,name='search_courses'),
path('accounts/profile',views.profile,name='profile'),
path('accounts/profile/update',views.profile_update,name='profile_update'),
path('products/filter_courses',views.filter_courses,name='filter_courses'),
path('course/<slug:slug>',views.course_detalis,name='course_details'),
path('error/404',views.page_not_found,name='error'),
path('assignment/<slug:slug>',views.assignment,name='assignment'),
path('discuss/<slug:slug>',views.discuss,name="discuss"),
path ('froala_editor/', include ( 'froala_editor.urls' ) ),
path('game/',views.game,name='game'),
path('game2/',views.game2,name='game2'),
path('treasure_hunt/',views.treasure_hunt,name='treasure_hunt'),
path('enrollment/<slug:slug>',views.enrollment,name="enrollment"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
