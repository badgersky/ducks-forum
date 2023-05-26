from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, DetailView

from forum.models import Thread, Comment, LikeComment, LikeThread
from forum.forms import AddCommentForm
from forum.permissions import ThreadCreatorRequiredMixin, CommentCreatorRequiredMixin


class DisplayThreadsView(ListView):
    model = Thread
    template_name = 'forum/list-threads.html'
    context_object_name = 'threads'
    paginate_by = 20


class CreateThreadView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ('subject', 'content')
    template_name = 'forum/create-thread.html'
    success_url = reverse_lazy('forum:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.request.user.score = F('score') + 5
        self.request.user.save()
        return super().form_valid(form)


class ThreadDetailsView(DetailView):
    """View for thread details, comments"""

    model = Thread
    template_name = 'forum/thread-details.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(thread_id=kwargs.get('object').pk)
        context['form'] = AddCommentForm
        return context


class AddCommentView(LoginRequiredMixin, CreateView):
    """View for adding comment to thread"""

    form_class = AddCommentForm
    template_name = 'forum/thread-details.html'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.request.user.score = F('score') + 2
        self.request.user.save()
        form.instance.user = self.request.user
        form.instance.thread = Thread.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['thread'] = Thread.objects.get(pk=self.kwargs.get('pk'))
        context['comments'] = Comment.objects.filter(thread_id=kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse('forum:details', kwargs={'pk': self.kwargs.get('pk')})

    def get_login_url(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'Login in order to add comment'
        )
        return reverse('users:login')


class DeleteThreadView(LoginRequiredMixin, ThreadCreatorRequiredMixin, DeleteView):
    model = Thread
    template_name = 'forum/delete-thread.html'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('forum:list')
    context_object_name = 'thread'


class DeleteCommentView(LoginRequiredMixin, CommentCreatorRequiredMixin, DeleteView):
    model = Comment
    template_name = 'forum/delete-comment.html'
    login_url = reverse_lazy('users:login')
    context_object_name = 'comment'

    def get_success_url(self):
        comment_id = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=comment_id)
        pk = comment.thread.id
        return reverse('forum:details', kwargs={'pk': pk})


class LikeCommentView(LoginRequiredMixin, View):
    """View checks if comment is already liked and increments number of likes"""
    login_url = reverse_lazy('users:login')

    def get(self, request, thr_pk, com_pk):
        try:
            comment = Comment.objects.get(pk=com_pk)
        except Comment.DoesNotExist:
            messages.add_message(
                request,
                messages.WARNING,
                f'Comment does not exist'
            )

            if Thread.objects.filter(pk=thr_pk).exists():
                return redirect(reverse('forum:details', kwargs={'pk': thr_pk}))

            return redirect(reverse('forum:list'))

        if not LikeComment.objects.filter(user=request.user, comment=comment).exists():
            LikeComment.objects.create(user=request.user, comment=comment)
            comment.likes = F('likes') + 1
            comment.user.score = F('score') + 1
            comment.user.save()
            comment.save()

        if Thread.objects.filter(pk=thr_pk).exists():
            return redirect(reverse('forum:details', kwargs={'pk': thr_pk}))

        return redirect(reverse('forum:list'))

    def get_login_url(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'Login in order to like comment'
        )
        return super().get_login_url()


class LikeThreadView(LoginRequiredMixin, View):
    """View checks if thread is already liked and increments number of likes"""
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        try:
            thread = Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            messages.add_message(
                request,
                messages.WARNING,
                f'Thread does not exist'
            )

            return redirect(reverse('forum:list'))

        if not LikeThread.objects.filter(user=request.user, thread=thread).exists():
            LikeThread.objects.create(user=request.user, thread=thread)
            thread.likes = F('likes') + 1
            thread.creator.score = F('score') + 1
            thread.creator.save()
            thread.save()

        return redirect(reverse('forum:details', kwargs={'pk': pk}))

    def get_login_url(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'Login in order to like thread'
        )
        return super().get_login_url()
