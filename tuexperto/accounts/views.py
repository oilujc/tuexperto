# from .forms import (PostForm, PageForm)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, resolve
from django.views.generic import (TemplateView,FormView,ListView,DetailView,View)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from meta.views import MetadataMixin
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

class ProfileView(HitCountDetailView):
	model = get_user_model()
	count_hit = True
	# slug_field = 'username'
	
	def get_template_names(self):
		template = 'account/profile.html'
		return template

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)

		obj = self.get_object()

		if obj.get_full_name():
			context['title_page'] = obj.get_full_name()
		else:	
			context['title_page'] = obj.username.title()
		context['breadcrumb'] = [(reverse_lazy('home'),'home'), ('',context['title_page'])]

		context['meta'] = self.get_object().as_meta(self.request)

		posts = self.get_object().post_set.filter(is_active=True, 
													post_type="pt").order_by('-created_at')

		page = self.request.GET.get('page', 1)

		paginator = Paginator(posts, 6)
		try:
			post = paginator.page(page)
		except PageNotAnInteger:
			post = paginator.page(1)
		except EmptyPage:
			post = paginator.page(paginator.num_pages)

		context['object_list'] = post

		return context

	# def get_queryset(self):
	# 	return get_user_model().objects.filter(is_active=True)

	def get_object(self, queryset=None):
		return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))