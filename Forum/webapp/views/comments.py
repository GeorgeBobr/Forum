from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from webapp.models import Topic, Reply
from webapp.forms import TopicForm, ReplyForm
class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply/reply_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:topic_detail', kwargs={'pk': self.kwargs['topic_id']})

class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply/reply_update.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('webapp:topic_detail', kwargs={'pk': self.object.topic.pk})

class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reply
    template_name = 'reply/reply_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('webapp:topic_detail', kwargs={'pk': self.object.topic.pk})