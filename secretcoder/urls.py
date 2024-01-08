"""
URL configuration for secretcoder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from .import views, user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.BASE, name='base'),
    path('', views.Home, name='home'),

    path('about', views.About, name='about'),
    path('contact', views.Contact_us, name='contact'),
    path('courses', views.courses, name='courses'),
    path('instructor', views.instructor, name='instructor'),
    path('form', views.form, name='form'),

    path('courses/filter-data', views.filter_data, name="filter-data"),
    path('search', views.search_course, name="search_course"),
    path('course/<slug:slug>', views.course_details, name='course_details'),



    path('testimonial', views.testimonial, name='testimonial'),
    path('editor', views.editor, name='editor'),
    path('404', views.pagenotfound, name='404'),
    path('team', views.team, name='team'),
    path('accounts/register', user_login.Register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', user_login.Login, name='login'),
    path('logout', user_login.logout_view, name='logout'),
    path('accounts/profile', user_login.profile, name='profile'),
    path('accounts/profile/update',
         user_login.profile_update, name='profile_update'),

    path('checkout/<slug:slug>', views.checkout, name='checkout'),
    path('my-course', views.my_course, name='my-course'),
    path('course/watch-course/<slug:slug>',
         views.watch_course, name='watch_course'),
    path("course/watch-course/comment/<int:id>",
         views.add_comment, name="add_comment"),

    path('editor', views.editor, name='editor'),
    path('terms-&-conditions', views.tc, name='terms-&-conditions'),
    path('faq', views.faq, name='faq'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),

    path('add_review/', views.add_review, name='add_review'),
    path('create_review', views.create_review, name='create_review'),

    path('verify_payment', views.verify_payment, name='verify_payment'),
    path('success', views.success, name='success'),
    path('subscriber', views.subscriber, name='subscriber'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
