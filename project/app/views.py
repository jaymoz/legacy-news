from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count,Q
from .forms import *
from django.http import HttpResponse
from djangorave.models import PaymentTypeModel
from django.contrib import messages
from django.http import HttpResponse
import json
from django.conf import settings
from json import dumps


def get_author(user):
	qs = Author.objects.filter(user=user)
	if qs.exists():
		return qs[0]
	return None

def search(request):
	queryset = Post.objects.all()
	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(
			Q(title__icontains=query)|
			Q(overview__icontains=query)
		).distinct()
	context = {'queryset':queryset}
	return render(request, 'app/search_result.html', context)

def get_category_count():
	#.values here returns only the category fields of each post, annonotate returns a dictionary
	queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
	
	return queryset


def home(request):
	footer = FooterLinks.objects.all()
	images = Images.objects.all()
	featured = Post.objects.filter(featured=True)
	latest = Post.objects.order_by('-timestamp')[0:3]
	team_info = TeamInfo.objects.all()
	about_text = HomepageAboutText.objects.all()

	context = {'object_list':featured,
				'latest':latest,
				'team_info':team_info,
				'images':images,
				'footer':footer,
				'about_text':about_text
				}
	return render(request, 'app/home.html', context)

def blog(request):
	footer = FooterLinks.objects.all()
	images = Images.objects.all()
	category_count = get_category_count()
	most_recent = Post.objects.order_by('-timestamp')[0:3]
	post_list = Post.objects.all()
	paginator = Paginator(post_list, 12)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)

	context = {'queryset':paginated_queryset,
			'page_request_var':page_request_var,
			'most_recent':most_recent,
			'category_count':category_count,
			'images':images,
			'footer':footer
			}
	return render(request, 'app/blog.html', context)

def post(request, id):
	footer = FooterLinks.objects.all()
	images = Images.objects.all()
	category_count = get_category_count()
	most_recent = Post.objects.order_by('-timestamp')[0:3]
	post = get_object_or_404(Post, id=id)

	if request.user.is_authenticated:
		PostView.objects.get_or_create(user=request.user, post=post)
	form = CommentForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.instance.user = request.user
			form.instance.post = post
			form.save()
			return redirect(reverse('post-detail',kwargs={'id':post.id}))

	context = {'post':post,
			'most_recent':most_recent,
			'category_count':category_count,
			'form':form,
			'images':images,
			'footer':footer,}
	return render(request, 'app/post.html', context)

def post_create(request):
	footer = FooterLinks.objects.all()
	images = Images.objects.all()
	title = 'Create'
	form = PostForm(request.POST or None, request.FILES or None)
	author = get_author(request.user)
	if request.method == "POST":
		if form.is_valid():
			form.instance.author = author
			form.save()
			return redirect(reverse("post-detail", kwargs={
				'id': form.instance.id
			}))
	context = {
		'title': title,
		'form': form,
		'images':images,
		'footer':footer
	}
	return render(request, "app/post_create.html", context)


def post_update(request, id):
	footer = FooterLinks.objects.all()
	images = Images.objects.all()
	title = 'Update'
	post = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None,instance=post)
	author = get_author(request.user)
	if request.method == "POST":
		if form.is_valid():
			form.instance.author = author
			form.save()
			messages.success(request, "This Post has been Updated!")
			return redirect(reverse("post-detail", kwargs={
				'id': form.instance.id
			}))
	context = {
		'title': title,
		'form': form,
		'images':images,
		'footer':footer
	}
	return render(request, "app/post_create.html", context)


def post_delete(request, id):
	post = get_object_or_404(Post, id=id)
	post.delete()
	messages.success(request, "This Post has been deleted!")
	return redirect(reverse("blog"))

def contact(request):
	footer = FooterLinks.objects.all()
	images = Images.objects.all()
	form = ContactForm()
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			email = form.cleaned_data.get('email')
			message = form.cleaned_data.get('message')
			try:
				contact = Contact()
				contact.name = name
				contact.email = email
				contact.message = message
				contact.save()
				messages.success(request, "You response has been received, we will contact you shortly!")
				return redirect("contact")
			except ObjectDoesNotExist:
				messages.warning(request, "Please ensure to fill in the valid details!")
				return redirect("contact")
	else:
		form = ContactForm()

	context = {'form':form,'images':images,'footer':footer}
	return render(request, 'app/contact.html' ,context)

def category(request):
	categories = Category.objects.all()
	category_count = get_category_count()
	footer = FooterLinks.objects.all()
	most_recent = Post.objects.order_by('-timestamp')[0:3]
	post_list = Post.objects.all()
	paginator = Paginator(post_list, 12)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)

	context = {'queryset':paginated_queryset,
			'page_request_var':page_request_var,
			'most_recent':most_recent,
			'category_count':category_count,
			'footer':footer,
			'categories':categories,
			}

	return render(request, 'app/category.html', context)


def category_detail(request, slug):
	category = Category.objects.get(slug=slug)
	category_posts = Post.objects.filter(categories=category)
	category_count = get_category_count()
	footer = FooterLinks.objects.all()
	most_recent = Post.objects.order_by('-timestamp')[0:3]
	post_list = Post.objects.all()
	paginator = Paginator(post_list, 12)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)

	context = {'queryset':paginated_queryset,
			'page_request_var':page_request_var,
			'most_recent':most_recent,
			'category_count':category_count,
			'footer':footer,
			'category_posts':category_posts
			}
	
	return render(request, "app/category-detail.html", context)