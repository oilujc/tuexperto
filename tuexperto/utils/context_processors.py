from blog.models import (Category,SubCategory, Post)
# from pages.models import (Page,)

# The context processor function
def categories(request):
	all_categories = Category.objects.all()[:10]

	return {
        'categories': all_categories,
	}

def pages(request):
	all_pages = Post.objects.filter(is_active=True, post_type="pg")[:10]

	return {
        'pages': all_pages,
	}


def last_post(request):
	all_pages = Post.objects.filter(is_active=True, post_type="pt").order_by('-created_at')[:5]

	return {
        'last_post': all_pages,
	}
