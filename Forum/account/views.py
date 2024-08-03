from django.shortcuts import redirect, reverse
from django.contrib.auth import login, get_user_model
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from account.forms import MyUserCreationForm, ProfileChangeForm
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordChangeView
from webapp.models import Topic, Reply  # Импортируйте ваши модели

User = get_user_model()

class RegistrationView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'register/registration.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if not next_page:
            next_page = self.request.POST.get('next')
        if not next_page:
            next_page = reverse('webapp:index')
        return next_page


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # Получение количества комментариев
        comment_count = Reply.objects.filter(author=user).count()
        context['comment_count'] = comment_count

        # Получение топиков пользователя
        topics = Topic.objects.filter(author=user)
        context['topics'] = topics

        # Пагинация для топиков
        paginator = Paginator(topics, 10)  # Показывать по 10 топиков на странице
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()

        return context


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileChangeForm
    template_name = 'user/user_change.html'
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})

class UserPasswordChangeView(UserPassesTestMixin, PasswordChangeView):
    template_name = 'user/user_password_change.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})
