from django.contrib.auth.decorators import login_required
from django.http import Http404


class StaffRequiredMixin(object):
	"""
	View mixin which requires that the authenticated user is a super user
	(i.e. `is_superuser` is True).
	"""

	@login_required
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			raise Http404
		return super(StaffRequiredMixin, self).dispatch(request,*args, **kwargs)