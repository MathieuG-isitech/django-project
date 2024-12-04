import logging
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from django.utils.text import slugify
from .forms import CategoryForm
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Configure le logger
logger = logging.getLogger('app')

def home(request):
    logger.info("Accès à la page d'accueil.")
    posts = Post.objects.all()
    logger.debug(f"{len(posts)} posts récupérés depuis la base de données.")
    
    # Ajouter LANGUAGE_CODE au contexte
    context = {
        'posts': posts,
        'LANGUAGE_CODE': get_language(),  # Ajout de LANGUAGE_CODE au contexte
    }
    
    return render(request, 'blog/home.html', context)

def post(request):
    logger.info("Accès à la page de détail d'un post.")
    return render(request, 'blog/post.html')

@login_required
def post_form(request):
    if request.method == 'POST':
        logger.info("Requête POST reçue pour créer un post.")
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        if not title or not content or not category_id:
            logger.warning("Données incomplètes pour créer un post.")
            return render(request, 'blog/post_form.html', {'error': 'Veuillez remplir tous les champs.'})

        try:
            category = Category.objects.get(id=category_id)
            author = request.user
            slug = slugify(title)
            post = Post.objects.create(
                title=title, 
                content=content, 
                category=category, 
                slug=slug, 
                status='draft', 
                author=author
            )
            logger.info(f"Post créé avec succès : {post.title} par {author.username}.")
            return redirect('blog-home')
        except Category.DoesNotExist:
            logger.error(f"Catégorie avec l'ID {category_id} introuvable.")
            return render(request, 'blog/post_form.html', {'error': 'Catégorie invalide.'})
        except Exception as e:
            logger.error(f"Erreur lors de la création du post : {str(e)}")
            return render(request, 'blog/post_form.html', {'error': 'Une erreur est survenue.'})

    categories = Category.objects.all()
    logger.debug(f"{len(categories)} catégories récupérées pour le formulaire de post.")
    return render(request, 'blog/post_form.html', {'categories': categories})

@login_required
def delete_post(request, post_id):
    logger.info(f"Tentative de suppression du post ID {post_id}.")
    post = get_object_or_404(Post, id=post_id)
    try:
        post.delete()
        logger.info(f"Post ID {post_id} supprimé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du post ID {post_id} : {str(e)}")
        return redirect('blog-home')
    return redirect('blog-home')

def login_view(request):
    logger.info("Accès à la page de connexion.")
    if request.method == "POST":
        logger.info("Tentative de connexion.")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"Utilisateur connecté : {username}.")
                return redirect('blog-home')
            else:
                logger.warning(f"Échec de connexion pour l'utilisateur : {username}.")
        else:
            logger.warning("Formulaire de connexion invalide.")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login/login.html', {'form': form})

def signup_view(request):
    logger.info("Accès à la page d'inscription.")
    if request.method == "POST":
        logger.info("Tentative d'inscription.")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("Nouvel utilisateur inscrit avec succès.")
            return redirect('login')
        else:
            logger.warning("Formulaire d'inscription invalide.")
    else:
        form = UserCreationForm()
    return render(request, 'blog/login/signup.html', {'form': form})

def logout_view(request):
    logger.info(f"Utilisateur {request.user.username} déconnecté.")
    logout(request)
    return redirect('login')

def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    logger.debug(f"Détails du post récupérés : {post.title}.")
    return render(request, 'blog/post_details.html', {'post': post})

def edit_post(request, post_id):
    logger.info(f"Accès à l'édition du post ID {post_id}.")
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author and not request.user.is_superuser:
        return redirect('blog-home')

    if request.method == 'POST':
        logger.info(f"Mise à jour du post ID {post_id} par {request.user.username}.")
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        try:
            category = Category.objects.get(id=category_id)
            post.title = title
            post.content = content
            post.category = category
            post.save()
            logger.info(f"Post ID {post_id} mis à jour avec succès.")
        except Category.DoesNotExist:
            logger.error(f"Catégorie avec ID {category_id} introuvable lors de l'édition du post ID {post_id}.")
            return redirect('blog-home')
        except Exception as e:
            logger.error(f"Erreur lors de l'édition du post ID {post_id} : {str(e)}.")
            return redirect('blog-home')

        return redirect('blog-home')
    else:
        categories = Category.objects.all()
        logger.debug(f"{len(categories)} catégories récupérées pour l'édition.")
        return render(request, 'blog/edit_post.html', {'post': post, 'categories': categories})
    
    
    
    
# CRUD catégorie

@login_required
def category_list(request):
    logger.info("Accès à la liste des catégories.")
    categories = Category.objects.all()
    logger.debug(f"{len(categories)} catégories récupérées depuis la base de données.")
    return render(request, 'blog/admin/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')

        if nom and description:
            slug = slugify(nom)
            if not Category.objects.filter(slug=slug).exists():
                Category.objects.create(nom=nom, description=description, slug=slug)
                logger.info(f"Catégorie créée : {nom} (slug: {slug})")
                return redirect('category-list')
            else:
                logger.warning(f"Le slug '{slug}' existe déjà. Nom de catégorie : {nom}")
                return render(request, 'blog/admin/category_create.html', {
                    'error': f"Une catégorie avec le slug '{slug}' existe déjà."
                })

    return render(request, 'blog/admin/category_create.html')

@login_required
def edit_category(request, category_id):
    logger.info(f"Accès à la modification de la catégorie ID {category_id}.")
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        logger.info(f"Requête POST reçue pour modifier la catégorie ID {category_id}.")
        nom = request.POST.get('nom')
        description = request.POST.get('description')

        if nom:
            category.nom = nom
            logger.debug(f"Le nom de la catégorie a été mis à jour : {nom}.")
            if description:
                category.description = description
                logger.debug(f"La description de la catégorie a été mise à jour : {description}.")
            category.save()
            logger.info(f"Catégorie ID {category_id} mise à jour.")
            return redirect('category-list')
        else:
            logger.warning(f"Nom manquant lors de la mise à jour de la catégorie ID {category_id}.")

    return render(request, 'blog/admin/category_edit.html', {'category': category})

@login_required
def delete_category(request, category_id):
    logger.info(f"Tentative de suppression de la catégorie ID {category_id}.")
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    logger.info(f"Catégorie ID {category_id} supprimée avec succès.")
    return redirect('category-list')

