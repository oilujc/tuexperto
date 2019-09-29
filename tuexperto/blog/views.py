from .forms import (PostForm, PageForm)
from .models import (Post, Category, SubCategory)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, resolve
from django.views.generic import (TemplateView,FormView,ListView,DetailView,View)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from meta.views import MetadataMixin
from utils.validators import VALID_POST_TYPE_LIST
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.db.models import Q

# Create your views here.
class SearchView(HitCountMixin,MetadataMixin,ListView):
	model = Post
	template_name= "blog/search.html"
	paginate_by = 9


	title="Buscar"
	description='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sequi explicabo aperiam rerum, quos consequuntur voluptatem voluptatum debitis ea recusandae voluptatibus ab itaque hic eius iste nobis, eos reprehenderit quae saepe!'
	keywords=['blog', 'informacion', 'increible']
	extra_props = {
	    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
	   	}
	extra_custom_props=[
	    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
	   	]


	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)

		context['qs'] = self.request.GET.get('q', None)
		if context['qs'] != None:
			context['title_page'] = "Resultados de {}".format(context['qs'])
		else:
			context['title_page'] = "Buscar"



		context['breadcrumb'] = [(reverse_lazy('home'),'home'), ('','Buscar')]
		return context

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)


	def get_queryset(self):
		qs = self.request.GET.get('q', None)

		posts = Post.objects.filter(is_active=True, 
									post_type="pt")

		if qs != None:
			posts =  posts.filter(
				Q(title__contains=qs) | 
				Q(description__contains=qs) |
				Q(content__contains=qs) |
				Q(tags__tag__contains=qs)
				)

		return posts.distinct().order_by('-created_at')

class PostView(HitCountDetailView):
	model = Post
	count_hit = True
	
	def get_template_names(self):
		template = 'blog/page_detail.html'
		return template


	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# context['related_post'] =
		context['meta'] = self.get_object().as_meta(self.request)
		return context

	def get_queryset(self):
		return Post.objects.filter(is_active=True)

class UserPostListView(LoginRequiredMixin, MetadataMixin, ListView):
	template_name= "blog/user_post_list.html"
	model = Post
	paginate_by = 5

	title="TuExperto.pro"
	description='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sequi explicabo aperiam rerum, quos consequuntur voluptatem voluptatum debitis ea recusandae voluptatibus ab itaque hic eius iste nobis, eos reprehenderit quae saepe!'
	extra_props = {
	    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
	   	}
	extra_custom_props=[
	    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
	   	]

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated != True:
			raise Http404

		if (self.request.user.user_type != 'bl' and 
			self.request.user.is_superuser != True and 
			self.request.user.is_staff != True):
			raise Http404

		if self.kwargs['pt'] in VALID_POST_TYPE_LIST:

			if VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'] != 'all':
				result = getattr(self.request.user, 
								VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'])

				if result != True:
					raise Http404

			return super().dispatch(*args, **kwargs)

		raise Http404


	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)

		title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['plural_title']
		single_title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['single_title']


		context['new_btn'] = "Crear {}".format(single_title)
		context['single_title'] = "{}".format(single_title)
		context['title_page'] = "Mis {}".format(title)
		context['breadcrumb'] = [(reverse_lazy('home'),'Inicio'), 
								('',"Mis {}".format(title))]

		context['post_type'] = self.kwargs['pt']

		return context

	def get_queryset(self):
		return Post.objects.filter(post_type=VALID_POST_TYPE_LIST[self.kwargs['pt']]['qs'], 
									user=self.request.user).order_by('-created_at')


class PostCreateView(LoginRequiredMixin, MetadataMixin, CreateView):
	model = Post
	template_name = "blog/post_new.html"

	title="TuExperto.pro"
	description='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sequi explicabo aperiam rerum, quos consequuntur voluptatem voluptatum debitis ea recusandae voluptatibus ab itaque hic eius iste nobis, eos reprehenderit quae saepe!'
	extra_props = {
	    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
	   	}
	extra_custom_props=[
	    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
	   	]

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated != True:
			raise Http404

		if (self.request.user.user_type != 'bl' and 
			self.request.user.is_superuser != True and 
			self.request.user.is_staff != True):
			raise Http404

		if self.kwargs['pt'] in VALID_POST_TYPE_LIST:

			if VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'] != 'all':
				result = getattr(self.request.user, 
								VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'])

				if result != True:
					raise Http404

			return super().dispatch(*args, **kwargs)

		raise Http404

	def get_success_url(self):
		return reverse_lazy('user_post', kwargs = {'pt': self.kwargs['pt']})

	def get_form_class(self):
		forms = {
			'page': PageForm,
			'post': PostForm,
		}
		return forms[self.kwargs['pt']]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		single_title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['single_title']
		plural_title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['plural_title']

		context['title_page'] = 'Nueva {}'.format(single_title)
		context['breadcrumb'] = [(reverse_lazy('home'),'Inicio'), 
								(reverse_lazy('user_post', kwargs={'pt': self.kwargs['pt']}),'Mis {}'.format(plural_title)), 
								('','Nueva {}'.format(single_title))]

		return context

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.instance.user = self.request.user
		form.instance.post_type = VALID_POST_TYPE_LIST[self.kwargs['pt']]['qs']
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, MetadataMixin, UpdateView):
	model = Post
	template_name = "blog/post_new.html"

	title="TuExperto.pro"
	description='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sequi explicabo aperiam rerum, quos consequuntur voluptatem voluptatum debitis ea recusandae voluptatibus ab itaque hic eius iste nobis, eos reprehenderit quae saepe!'
	extra_props = {
	    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
	   	}
	extra_custom_props=[
	    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
	   	]

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated != True:
			raise Http404

		if (self.request.user.user_type != 'bl' and 
			self.request.user.is_superuser != True and 
			self.request.user.is_staff != True):
			raise Http404


		if self.kwargs['pt'] in VALID_POST_TYPE_LIST:

			if VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'] != 'all':
				result = getattr(self.request.user, 
								VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'])

				if result != True:
					raise Http404

			return super().dispatch(*args, **kwargs)

		raise Http404

	def get_queryset(self):
		return Post.objects.filter(post_type=VALID_POST_TYPE_LIST[self.kwargs['pt']]['qs'], 
									user=self.request.user).order_by('-created_at')

	def get_success_url(self):
		return reverse_lazy('user_post', kwargs = {'pt': self.kwargs['pt']})

	def get_form_class(self):
		forms = {
			'page': PageForm,
			'post': PostForm,
		}
		return forms[self.kwargs['pt']]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page = self.get_object()
		single_title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['single_title']
		plural_title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['plural_title']

		context['title_page'] = 'Editar {}'.format(page.title.title())
		context['breadcrumb'] = [(reverse_lazy('home'),'Inicio'), 
								(reverse_lazy('user_post', kwargs={'pt': self.kwargs['pt']}),'Mis {}'.format(plural_title)), 
								('','Editar {}'.format(page.title.title()))]

		return context

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.instance.user = self.request.user
		form.instance.post_type = VALID_POST_TYPE_LIST[self.kwargs['pt']]['qs']
		return super().form_valid(form)



class PostDeleteView(LoginRequiredMixin, MetadataMixin, DeleteView):
	model = Post
	template_name = "blog/post_delete.html"

	title="TuExperto.pro"
	description='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sequi explicabo aperiam rerum, quos consequuntur voluptatem voluptatum debitis ea recusandae voluptatibus ab itaque hic eius iste nobis, eos reprehenderit quae saepe!'
	extra_props = {
	    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
	   	}
	extra_custom_props=[
	    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
	   	]

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated != True:
			raise Http404

		if (self.request.user.user_type != 'bl' and 
			self.request.user.is_superuser != True and 
			self.request.user.is_staff != True):
			raise Http404


		if self.kwargs['pt'] in VALID_POST_TYPE_LIST:

			if VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'] != 'all':
				result = getattr(self.request.user, 
								VALID_POST_TYPE_LIST[self.kwargs['pt']]['permission'])

				if result != True:
					raise Http404

			return super().dispatch(*args, **kwargs)

		raise Http404

	def get_queryset(self):
		return Post.objects.filter(post_type=VALID_POST_TYPE_LIST[self.kwargs['pt']]['qs'], 
									user=self.request.user).order_by('-created_at')

	def get_success_url(self):
		return reverse_lazy('user_post', kwargs = {'pt': self.kwargs['pt']})


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page = self.get_object()
		single_title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['single_title']
		plural_title = VALID_POST_TYPE_LIST[self.kwargs['pt']]['plural_title']

		context['title_page'] = 'Eliminar {}'.format(page.title.title())
		context['breadcrumb'] = [(reverse_lazy('home'),'Inicio'), 
								(reverse_lazy('user_post', kwargs={'pt': self.kwargs['pt']}),'Mis {}'.format(plural_title)), 
								('','Eliminar {}'.format(page.title.title()))]

		return context


class CategoryView(HitCountDetailView):

	model = Category
	template_name= "blog/blog.html"
	count_hit = True

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)

		context['title_page'] = self.get_object().category.title()
		context['breadcrumb'] = [(reverse_lazy('home'),'home'), ('',context['title_page'])]

		posts = self.get_object().post_set.filter(is_active=True, 
													post_type="pt").order_by('-created_at')

		page = self.request.GET.get('page', 1)

		paginator = Paginator(posts, 9)
		try:
			post = paginator.page(page)
		except PageNotAnInteger:
			post = paginator.page(1)
		except EmptyPage:
			post = paginator.page(paginator.num_pages)

		context['object_list'] = post

		context['meta'] = self.get_object().as_meta(self.request)
		return context

class SubCategoryView(HitCountDetailView):

	model = SubCategory
	template_name= "blog/blog.html"
	count_hit = True

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		obj = self.get_object()
		context['title_page'] = obj.subcategory.title()
		context['breadcrumb'] = [('home','home'), 
								(reverse_lazy('category', kwargs = {'slug': obj.category.slug}) ,obj.category.category.title()), 
								('',obj.subcategory.title())]

		posts = Post.objects.filter(is_active=True,
									category__slug=self.kwargs['category'],
									subcategory=self.get_object(),
									post_type="pt").order_by('-created_at')

		page = self.request.GET.get('page', 1)

		paginator = Paginator(posts, 9)
		try:
			post = paginator.page(page)
		except PageNotAnInteger:
			post = paginator.page(1)
		except EmptyPage:
			post = paginator.page(paginator.num_pages)

		context['object_list'] = post



		context['meta'] = self.get_object().as_meta(self.request)
		return context