from django.shortcuts import redirect, reverse
from django.contrib.auth import login, get_user_model
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from account.forms import MyUserCreationForm, ProfileChangeForm
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordChangeView

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
        user = self.object
        posts = user.post_set.order_by('-created_at')
        paginator = Paginator(posts, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        comment_count = user.comment_set.count()

        kwargs['page_obj'] = page
        kwargs['posts'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        kwargs['comment_count'] = comment_count
        return super().get_context_data(**kwargs)


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
