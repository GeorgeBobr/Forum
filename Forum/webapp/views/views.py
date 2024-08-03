from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from webapp.models import Topic, Reply
from webapp.forms import TopicForm, ReplyForm

class TopicListView(ListView):
    model = Topic
    template_name = 'topic/index.html'
    context_object_name = 'topics'
    ordering = ['-created_at']



class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topic/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = context['topic'].replies.all()
        context['reply_form'] = ReplyForm()
        return context

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'topic/topic_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:index')

class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'topic/topic_update.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('webapp:topic_detail', kwargs={'pk': self.object.pk})

class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Topic
    template_name = 'topic/topic_delete.html'
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user == self.get_object().author