from django.shortcuts import render, \
    get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, reverse
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy




# Create your views here.

# def home(request):
#     return HttpResponse(content='hello world.')


# def home(request):
#     boards = Board.objects.all()
#     boards_names = []
#
#     for board in boards:
#         boards_names.append(board)
#
#     response_html = '<br>'.join(boards_names)
#     return HttpResponse(response_html)


# def home(request):
#     boards = Board.objects.all()
#     return render(request, 'home.html', {'boards': boards})

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


# def board_topics(request, pk):
#     try:
#         board = Board.objects.get(pk=pk)
#     except Board.DoesNotExist:
#         raise Http404
#     return render(request, 'topics.html', {'board': board})

# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     return render(request, 'topics.html', {'board':board})

# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     return render(request, 'new_topic.html', {'board': board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )

        # return redirect('board_topics', pk=board.pk) # TODO: redirect to the created topic page
        return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})



@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk':pk, 'topic_pk':topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                page=topic.get_page_count(),
                id=post.pk
            )
            # return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


# GCBV分页
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 2 # 每页的board个数

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset









