from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-date']


class WebsiteDetailView(DetailView):
    model = Post
    template_name = 'Selected_Website.html'


class AddWebsiteView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_websites.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateWebsiteView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_website.html'


class DeleteWebsiteView(DeleteView):
    model = Post
    template_name = 'delete_website.html'
    success_url = reverse_lazy('home')


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    success_url = reverse_lazy('home')
    ordering = ['-date']

    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)