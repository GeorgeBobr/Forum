from django.urls import path
from webapp.views.views import TopicListView, TopicDetailView, TopicCreateView, TopicUpdateView, TopicDeleteView
from webapp.views.comments import ReplyUpdateView, ReplyCreateView, ReplyDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', TopicListView.as_view(), name='index'),
    path('create/', TopicCreateView.as_view(), name='topic_create'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('<int:pk>/edit/', TopicUpdateView.as_view(), name='topic_update'),
    path('<int:pk>/delete/', TopicDeleteView.as_view(), name='topic_delete'),


    path('<int:topic_id>/reply/', ReplyCreateView.as_view(), name='reply_create'),
    path('reply/<int:pk>/edit/', ReplyUpdateView.as_view(), name='reply_update'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
]
