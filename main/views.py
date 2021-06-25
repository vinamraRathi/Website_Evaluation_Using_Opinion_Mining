from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Rating, evaluate_website, set_website_Rating
from .forms import PostForm, CommentForm, RatingForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from rest_framework.views import APIView


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-date']


class WebsiteDetailView(DetailView):
    model = Post
    template_name = 'Selected_Website.html'

    def get(self, request:HttpResponse, slug, pk):
        if request.method == 'GET':
            data2 = Comment.objects.values('post', 'body')
            evaluate_website(data2, pk)
        return super().get(request)


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

class ShowRating(UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'show_rating.html'
    fields = '__all__'

    def get_object(self, queryset=None):
        return get_object_or_404(Rating, pk=self.kwargs.get('pk'))

    def get(self, request:HttpResponse, slug, pk):
        if request.method == 'GET':
            return super().get(request)


class call_model(APIView):
    def get(self, request):
        if request.method == 'GET':
            data2 = Comment.objects.values('post', 'body')
            print(data2)
            data = set_website_Rating(data2)
            for x in data:
                r = Rating.objects.update_or_create(post_id = x[0], rating = x[1])
                print(r)
            return JsonResponse(data, safe=False)                