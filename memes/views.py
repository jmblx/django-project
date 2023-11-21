from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.views.generic.base import View

from .form import CommentsForm, AddMemForm, RegisterUserForm, LoginUserForm, ContactForm, UpdateMemesForm
from .models import Memes, Category
from .utils import DataMixin


# Create your views here.

# class MemesView(View):
#     '''Вывод мемов'''
#     def get(self, request):
#         memes = Memes.objects.all()
#         return render(request, 'memsite/memsite.html', {'mem_list': memes, 'title': 'Балдёжные мэмы', 'theme_selected': 'Главная'})

class MemesView(DataMixin, ListView):
    '''Вывод мемов'''
    model = Memes
    template_name = 'memsite/memsite.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Балдёжные мэмы', theme_selected='Главная')
        return dict(list(context.items()) + list(c_def.items()))

# class Show_category(View):
#     '''Отдельная категория'''
#     def get(self, request, cat_slug):
#
#         cat_selected = Category.objects.all().get(slug=cat_slug)
#         cat_id = cat_selected.id
#         memes = Memes.objects.filter(cat_id=cat_id)
#
#         if len(memes) == 0:
#             raise Http404()
#
#         return render(request, 'memsite/cat_selected.html', {'mems': memes, 'cat_selected': cat_selected, 'title': 'a', 'theme_selected': cat_selected})

class ShowCategory(DataMixin, ListView):
    '''Отдельная категория'''
    model = Memes
    template_name = 'memsite/cat_selected.html'
    context_object_name = 'mems'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return Memes.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=f'Мемы категории {str(c.name)}', cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class AddComments(View):
    '''добавление комментариев'''
    def post(self, request, pk):
        form = CommentsForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.mem_id = pk
            form.save()
        mem = Memes.objects.all().get(id=pk)
        mem_slug = mem.slug
        return redirect(f'/mem/{mem_slug}/')

# class MemDetail(View):
#     '''Отдельный мем'''
#     def get(self, request, mem_slug):
#         mem = Memes.objects.get(slug=mem_slug)
#         return render(request, 'memsite/mem_detail.html', {'mem': mem, 'title': mem.name, 'theme_selected': mem.cat})

class MemDetail(DataMixin, DetailView):
    '''Отдельный мем'''
    model = Memes
    template_name = 'memsite/mem_detail.html'
    slug_url_kwarg = "mem_slug"
    context_object_name = 'mem'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['mem'].name)
        return dict(list(context.items()) + list(c_def.items()))

# def addmem(request):
#     if request.method == 'POST':
#         form = AddMemForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = AddMemForm()
#     return render(request, 'memsite/addmem.html', {'form': form, 'title': 'Добавить мем', 'url_name': 'add_mem', 'theme_selected': 'Добавить мем'})

class AddMem(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddMemForm
    template_name = 'memsite/addmem.html'
    login_url = '/admin/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить мем', update_mode=False)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateMem(LoginRequiredMixin, DataMixin, UpdateView):
    model = Memes
    form_class = UpdateMemesForm
    template_name = 'memsite/addmem.html'
    login_url = '/admin/'
    slug_field = 'slug'
    slug_url_kwarg = 'mem_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редактировать мем', update_mode=True, meme=self.get_object())
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'memsite/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация', update_mode=True)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'memsite/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

class ContactFormView(DataMixin, FormView):

    form_class = ContactForm
    template_name = 'memsite/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')