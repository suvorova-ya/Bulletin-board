from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import *
from .models import *


"""Главная страница"""

class BboardHome(ListView):
    model = Post
    template_name = 'project/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)

        """Отображение категорий на главной странице"""

class PostCategory(ListView):
    model = Post
    template_name = 'project/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'project/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(
            post=self.get_object()).order_by('-created')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
                                  author=self.request.user,
                                  post=self.get_object())

        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class PostCreateView(PermissionRequiredMixin,CreateView):
    model = Post
    template_name = 'project/create_post.html'
    form_class = PostForm
    permission_required = 'project.add_post'
    raise_exception = True
    success_url = '/list/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def add_image(request):
        if request.method == 'POST' and request.FILES:
           file = request.FILES['myfile1']
           fs = FileSystemStorage()
           filename = fs.save(file.name, file)
           file_url = fs.url(filename)
           return render(request, 'create_post.html', {
                'file_url': file_url
            })
        return render(request, 'create_post.html')





"""Обновление объявления"""

class PostUpdateView(PermissionRequiredMixin,UpdateView):
    model = Post
    template_name = 'project/create_post.html'
    form_class = PostForm
    permission_required = 'project.change_post'
    success_url = '/list/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

"""удаление объявления"""

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'project/post_delete.html'
    success_url = 'list'

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)



"""страница с откликами на  объявления пользователя"""
class ListPost(ListView):
    model = Post
    template_name = 'project/comment_list.html'
    context_object_name = 'board'
    ordering = '-created'
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = Comment.objects.filter(post__author=self.request.user)
        return context



"""фильтровать отклики по объявлениям, удалять их и принимать """
class CommentPost(DetailView):

    model = Post
    ordering = ['-creation']
    template_name = 'project/post_comment.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = Comment.objects.filter(post_id=self.kwargs.get('pk'))
        return context

"""принять комментарий к объявлению"""
@login_required
def accept(request, pk):
    Comment.objects.filter(post=pk).update(active=True)

    instance = Comment.objects.filter(post_id=pk)
    post_author = list(instance.values_list('post__author__username', flat=True))
    post_id = list(instance.values_list('post__id', flat=True))
    comment_user = list(instance.values_list("author__username", flat=True))
    email = list(instance.values_list("author__email", flat=True))

    send_mail(
        subject=post_author[0],
        message=f"Dear, {comment_user[0]}\n"
                f"Your comment to {post_author[0]}'s post has been accepted!",
        from_email='Django07.22@yandex.ru',
        recipient_list=[email[0]])

    return HttpResponseRedirect(f'/accounts/profile/post/{post_id[0]}/')


"""удалить комментарий к объявлению"""
class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'project/comment_delete.html'
    success_url = '/accounts/list/'