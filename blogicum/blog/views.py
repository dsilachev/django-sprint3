from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .models import Post, Category

POSTS_LIMIT = 5


def get_published_posts():
    return Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True,
    )


def index(request):
    posts = get_published_posts()[:POSTS_LIMIT]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, id):
    post = get_object_or_404(
        get_published_posts(),
        id=id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.select_related(
        'author',
        'category',
        'location'
    ).filter(
        is_published=True,
        pub_date__lte=now()
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': posts,
        }
    )
