"""tuexperto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import reverse_lazy
from django.conf.urls import handler404, handler500
from django.contrib.auth.views import (LoginView,
                                       LogoutView,)

from accounts.views import (ProfileView,)

from .views import (HomeView, register_view, activate, ContactFormView)
from blog.views import (PostView,
                        CategoryView,
                        SubCategoryView,
                        UserPostListView,
                        PostCreateView,
                        PostUpdateView,
                        PostDeleteView,
                        SearchView
                        )
from courses.views import (UserCourseListView,
                           UserCourseDetailView,
                           CoursePostCreateView,
                           CoursePostView,
                           CourseCreateView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('search/', SearchView.as_view(), name="search"),
    path('contact/', ContactFormView.as_view(), name="contact"),

    path('topic/<slug:slug>/', CategoryView.as_view(), name="category"),
    path('topic/<slug:category>/<slug:slug>',
         SubCategoryView.as_view(), name="subcategory"),
    path('<slug:slug>', PostView.as_view(), name="post"),

    path('courses/<slug:course>/<slug:slug>', CoursePostView.as_view(), name="course_post"),

    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),

    # Auth System
    path('account/signin/', LoginView.as_view(template_name='auth/login.html',
                                              redirect_authenticated_user=True,
                                              extra_context={'title_page': 'Sign in',
                                                             'breadcrumb': [(reverse_lazy('home'), 'Inicio'), 
                                                             ('', 'Iniciar Sesión')]}), name='signin'),

    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/signup/', register_view, name='signup'),

    path('account/courses/', UserCourseListView.as_view(), name='user_courses'),
    path('account/courses/<slug:slug>/', UserCourseDetailView.as_view(), name='user_courses_detail'),
    path('account/courses/<slug:course>/new', CoursePostCreateView.as_view(), name='user_courses_detail_new'),
    path('account/courses/new', CourseCreateView.as_view(), name='user_courses_new'),

    path('account/<slug:pt>/', UserPostListView.as_view(), name='user_post'),
    path('account/<slug:pt>/new', PostCreateView.as_view(), name='user_post_new'),
    path('account/<slug:pt>/<slug:slug>/edit',
         PostUpdateView.as_view(), name='user_post_edit'),
    path('account/<slug:pt>/<slug:slug>/delete',
         PostDeleteView.as_view(), name='user_post_delete'),


    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('select2/', include('django_select2.urls')),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),

    # Api
    path('api/blog/', include('blog.api.urls')),
    path('api/account/', include('accounts.api.urls')),

]
if settings.DEBUG:
    # static = Funcion auxiliar para devolver un patron de URL para servir archivos en modo debug
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'tuexperto.views.error_404'
