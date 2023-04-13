from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Category
from .forms import CommentForm, PostSearchForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers



def categories_processor(request):
    categories = Category.objects.exclude(name='default')
    data = {'categories': categories}
    return data



class CategoryListView(ListView):
    template_name = 'category.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        data = {
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published'), 
            'category': self.kwargs['category']
            }
        return data



def home(request):
    all_posts = Post.custom_manager.all()
    data = {'posts': all_posts}
    return render(request, 'home.html', data)



def post_single(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')


    all_comments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_comments, 10)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user_comment = form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
        else:
            data = {'error': 'form is not valid', 'form': f'{form}'}
            return JsonResponse(data)
    else:
        form = CommentForm()

    data = {'post': post, 'comments': user_comment, 'comments': comments, 'comment_form': form, 'all_comments': all_comments}
    return render(request, 'single_post.html', data)



def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()


    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))
        if search_string is not None:
            search_string = Post.objects.filter(title__contains=search_string)[:5]
            data = serializers.serialize('json', list(search_string), fields=('id', 'title', 'slug'))
            return JsonResponse({'search_string': data})

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)
            results = Post.objects.filter(query)

    return render(request, 'search.html', {'form': form, 'q': q, 'results': results,})