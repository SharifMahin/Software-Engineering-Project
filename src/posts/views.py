from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.forms import UserChangeForm
from .forms import CommentForm, PostForm,EditProfileForm,ProfileForm
from .models import Post, Author, PostView,Comment,Category
from marketing.models import Signup
from contactus.models import ContactUs


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
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)
    
def category(request,pk):
    categories = get_object_or_404(Category,pk=pk)
    queryset = Post.objects.filter(categories=categories)
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)

def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


def index(request):
    featured = Post.objects.filter(featured=True)
    approved = Post.objects.filter(is_approved=True)
    latest = approved.order_by('-timestamp')[0:3]
    category=Category.objects.all()

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'category': category
    }
    return render(request, 'index.html', context)

def blog(request):
    category=Category.objects.all()
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3] 
    post_list = Post.objects.filter(is_approved=True)
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    
    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'category':category
    }
    return render(request, 'blog.html', context)

def post(request, id):
    category=Category.objects.all()
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user,post=post)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'form': form,
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'category':category

    }
    return render(request, 'post.html', context)

def post_create(request):
    category=Category.objects.all()
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
        'category':category
    }
    return render(request, "post_create.html", context)

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None, 
        request.FILES or None, 
        instance=post)
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
        'form': form
    }
    return render(request, "post_create.html", context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))

def comment_delete(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', id=comment.post.id)


def profile(request):
    user = request.user
    user_author = get_author(request.user)
    user_posts = Post.objects.filter(author=user_author)

    context ={
        'user': user,
        'user_posts': user_posts
    }
    return render(request,"profile.html",context)

def edit_profile(request):
    author= get_author(request.user)
    form = EditProfileForm(request.POST or None, instance=request.user)
    ProForm = ProfileForm(request.POST or None,request.FILES or None, instance=author)
    if request.method == 'POST':

        if form.is_valid() and ProForm.is_valid():
            ProForm.save()
            form.save()
            return redirect(reverse('profile'))
    else:
        form = EditProfileForm(instance=request.user)
        ProForm = ProfileForm( request.FILES, instance=author)
        args = {
            'form': form,
            'proform': ProForm
            }
        return render(request, 'edit_profile.html', args)

def contact(request):
    if request.method =="POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        new_contact = ContactUs()
        new_contact.name = name
        new_contact.email = email
        new_contact.message = message
        new_contact.save()
        context = {
        'name': name,
        'email': email,
        'message': message
    }
        return render(request,"contact.html",context)
    else:
        return render(request,'contact.html',{})   

