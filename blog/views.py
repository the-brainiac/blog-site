from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.humanize.templatetags.humanize import naturaltime

from .owner import *
from blog.models import Blog, Comment, Fav
from user.models import Person
from .forms import CreateForm, CommentForm

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


from .utils import dump_queries
from django.db.models import Q

def filter_blogs(request, strval):
    if strval:
        # Simple title-only search
        # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

        # Multi-field search
        query = Q(title__contains=strval)
        query.add(Q(body__contains=strval), Q.OR)
        objects = Blog.objects.filter(
            query).select_related().order_by('-updated_at')
    else :
        # try both versions with > 4 posts and watch the queries that happen
        objects = Blog.objects.all().order_by('-updated_at')
        # objects = Ad.objects.select_related().all().order_by('-updated_at')[:10]
    dump_queries()
    return objects
from collections import Counter

class MainView(View):
    def get(self, request):
        strval =  request.GET.get("search", False)
        blogs = filter_blogs(request, strval)
        
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_blogs.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        trending_blogs = Counter(Blog.objects.all().order_by('-comment'))
        trending_blogs = sorted(trending_blogs.keys(), key=lambda x: -trending_blogs[x])[:5]

        ctx = {'blog_list': blogs, 'favorites':favorites, 'search':strval, 'trending_blogs':trending_blogs}
        return render(request, 'blog/blog_list.html', ctx)


class BlogCreateView(LoginRequiredMixin, View):
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blogs:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # add owner to the model before saving
        blog = form.save(commit=False)
        blog.owner = self.request.user
        blog.save()
        return redirect(self.success_url)


class BlogDetailView(View):
    model = Blog
    template_name = 'blog/blog_detail.html'
    def get(self, request, pk):
        x = Blog.objects.get(id=pk)
        comments = Comment.objects.filter(blog=x).order_by('updated_at')
        comment_form = CommentForm()
        context = { 'blog' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class BlogUpdateView(OwnerUpdateView):
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blogs:all')

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, owner=self.request.user)
        form = CreateForm(instance=blog)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        blog = get_object_or_404(Blog, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=blog)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        blog = form.save(commit=False)
        blog.save()

        return redirect(self.success_url)
    
class BlogDeleteView(OwnerDeleteView):
    model = Blog





class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Blog, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, blog=a)
        comment.save()
        url = reverse('blogs:detail', args=[pk]) + '#blog-comment'
        # print(url)
        return redirect(url)

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "blog/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        blog = self.object.blog
        return reverse('blogs:detail', args=[blog.id])



@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        a = get_object_or_404(Blog, id=pk)
        fav = Fav(user=request.user, blog=a)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        a = get_object_or_404(Blog, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, blog=a).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

