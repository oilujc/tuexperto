from .models import (Course,)
from .forms import (CourseForm, )
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, resolve
from django.views.generic import (
    TemplateView, FormView, ListView, DetailView, View)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from meta.views import MetadataMixin
from hitcount.views import HitCountDetailView, HitCountMixin
from hitcount.models import HitCount
from django.db.models import Q
from tuexperto.settings import TITLE_PAGE, GLOBAL_DESCRIPTION
from blog.models import Post
from blog.forms import PostForm
# Create your views here.


class UserCourseListView(LoginRequiredMixin, MetadataMixin, ListView):
    template_name = "blog/user_post_list.html"
    model = Course
    paginate_by = 5

    title = TITLE_PAGE
    description = GLOBAL_DESCRIPTION

    extra_props = {
        'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
    }
    extra_custom_props = [
        ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
    ]

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated != True:
            raise Http404

        if (self.request.user.is_superuser != True and
                self.request.user.is_staff != True):
            raise Http404

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['new_btn'] = 'Crear curso'
        context['new_btn_url'] = 'user_courses_new'
        context['single_title'] = 'curso'
        context['title_page'] = 'Mis cursos'
        context['breadcrumb'] = [(reverse_lazy('home'), 'Inicio'),
                                 ('', 'Mis cursos')]

        return context

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user).order_by('-created_at')


class CourseCreateView(LoginRequiredMixin, MetadataMixin, CreateView):
    model = Course
    template_name = "blog/post_new.html"

    title = TITLE_PAGE
    description = GLOBAL_DESCRIPTION

    extra_props = {
        'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
    }
    extra_custom_props = [
        ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
    ]

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated != True:
            raise Http404

        if (self.request.user.is_superuser != True and
                self.request.user.is_staff != True):
            raise Http404

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('user_courses')

    def get_form_class(self):
        return CourseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title_page'] = 'Nuevo curso'
        context['breadcrumb'] = [(reverse_lazy('home'), 'Inicio'),
                                 (reverse_lazy('user_courses'), 'Mis cursos'),
                                 ('', 'Nuevo curso')]

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserCourseDetailView(LoginRequiredMixin, MetadataMixin, DetailView):
    model = Course

    def get_template_names(self):
        template = 'courses/user_course_detail.html'
        return template

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['meta'] = self.get_object().as_meta(self.request)

        title = self.get_object().title
        context['title_page'] = title
        context['new_btn'] = 'Añadir entrada'
        context['breadcrumb'] = [(reverse_lazy('home'), 'Inicio'),
                                 (reverse_lazy('user_courses'), 'Mis cursos'),
                                 ('', title)]

        return context

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user).order_by('-created_at')

class CoursePostView(HitCountDetailView):
    model = Post
    count_hit = True

    def get_template_names(self):
        template = 'courses/course_page_detail.html'
        return template

    def get_course(self):
        try:
            return Course.objects.get(slug = self.kwargs['course'])
        except Course.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context

    def get_queryset(self):
        return self.get_course().posts.filter(is_active=True, post_type='co')


class CoursePostCreateView(LoginRequiredMixin, MetadataMixin, CreateView):
    model = Post
    template_name = "blog/post_new.html"

    title = TITLE_PAGE
    description = GLOBAL_DESCRIPTION

    extra_props = {
        'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
    }
    extra_custom_props = [
        ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
    ]

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated != True:
            raise Http404

        if (self.request.user.is_superuser != True and
                self.request.user.is_staff != True):
            raise Http404

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('user_courses_detail', kwargs={'slug': self.kwargs['course']})

    def get_form_class(self):
        return PostForm

    def get_course(self):
        try:
            return Course.objects.get(slug = self.kwargs['course'])
        except Course.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        single_title = 'Entrada'
        
        

        context['title_page'] = 'Nueva {}'.format(single_title)
        context['breadcrumb'] = [(reverse_lazy('home'), 'Inicio'),
                                (reverse_lazy('user_courses'), 'Mis cursos'),
                                (reverse_lazy('user_courses_detail', kwargs={'slug': self.kwargs['course']}),
                                self.get_course().title.capitalize()),
                                ('', 'Nueva entrada')
            ]

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        form.instance.post_type = 'co'

        form.instance.save()

        self.get_course().posts.add(form.instance)

        return super().form_valid(form)


