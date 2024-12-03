from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def post(request):
    return render(request, 'blog/post.html')

@login_required
def post_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category') 
        category = Category.objects.get(id=category_id) 
        author = request.user
        slug = slugify(title)
        

        post = Post.objects.create(title=title, content=content, category=category, slug=slug, status='draft', author=author)
        return redirect('blog-home')
    
    categories = Category.objects.all()
    return render(request, 'blog/post_form.html', {'categories': categories})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('blog-home')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  
                return redirect('blog-home')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login/login.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login')  
    else:
        form = UserCreationForm()
    
    return render(request, 'blog/login/signup.html', {'form': form})


def logout_view(request):
    logout(request) 
    return redirect('login')  

def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_details.html', {'post': post})

def edit_post(request, post_id):
    # Récupérer le post à éditer
    post = get_object_or_404(Post, id=post_id)

    # Vérification des permissions 
    if request.user != post.author and not request.user.is_superuser:
        return redirect('blog-home')  # Rediriger si l'utilisateur n'a pas l'autorisation

    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)

        # Mettre à jour les champs du post
        post.title = title
        post.content = content
        post.category = category

        
        post.save()

        return redirect('blog-home')

    else:
        categories = Category.objects.all()
        return render(request, 'blog/edit_post.html', {'post': post, 'categories': categories})
