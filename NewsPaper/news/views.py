from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-data_time_creation')
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post'


class PostSearch(PostList):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(CreateView):
    template_name = 'post_add.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '..'

