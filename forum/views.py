from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView

from forum import models, forms
from forum.permissions import ThreadCreatorRequiredMixin, CommentCreatorRequiredMixin


class DisplayThreadsView(ListView):
    model = models.Thread
    template_name = 'forum/list-threads.html'
    context_object_name = 'threads'


class CreateThreadView(LoginRequiredMixin, CreateView):
    model = models.Thread
    fields = ('subject', 'content')
    template_name = 'forum/create-thread.html'
    success_url = reverse_lazy('forum:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.request.user.score += 5
        self.request.user.save()
        return super().form_valid(form)


class ThreadDetailsView(View):

    def get(self, request, pk):
        try:
            thread = models.Thread.objects.get(pk=pk)
        except models.Thread.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'No such thread')

            return redirect(reverse('forum:list'))

        comments = models.Comment.objects.filter(thread=thread).order_by('-date_at')

        comment_form = forms.AddCommentForm

        return render(request, 'forum/thread-details.html', {'thread': thread,
                                                             'comments': comments,
                                                             'form': comment_form})


class AddCommentView(View):

    def post(self, request, pk):
        if request.user.is_authenticated:
            form = forms.AddCommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)

                comment.user = request.user
                try:
                    comment.thread = models.Thread.objects.get(pk=pk)
                except models.Thread.DoesNotExist:
                    messages.add_message(request,
                                         messages.WARNING,
                                         f'No such thread')

                    return redirect(reverse('forum:list'))

                request.user.score += 2
                request.user.save()

                form.save()

                return redirect(reverse('forum:details', kwargs={'pk': pk}))

        messages.add_message(request,
                             messages.WARNING,
                             f'Login if you want to add comment')

        return redirect(reverse('users:login'))


class DeleteThreadView(LoginRequiredMixin, ThreadCreatorRequiredMixin, DeleteView):
    model = models.Thread
    template_name = 'forum/delete-thread.html'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('forum:list')
    context_object_name = 'thread'


class DeleteCommentView(LoginRequiredMixin, CommentCreatorRequiredMixin, DeleteView):
    model = models.Comment
    template_name = 'forum/delete-comment.html'
    login_url = reverse_lazy('users:login')
    context_object_name = 'comment'

    def get_success_url(self):
        comment_id = self.kwargs.get('pk')
        comment = models.Comment.objects.get(pk=comment_id)
        pk = comment.thread.id
        return reverse('forum:details', kwargs={'pk': pk})


class LikeCommentView(View):

    def get(self, request, thr_pk, com_pk):
        if request.user.is_authenticated:
            try:
                comment = models.Comment.objects.get(pk=com_pk)
            except models.Comment.DoesNotExist:
                messages.add_message(request,
                                     messages.WARNING,
                                     f'Comment does not exist')

                if models.Thread.objects.filter(pk=thr_pk).exists():
                    return redirect(reverse('forum:details', kwargs={'pk': thr_pk}))

                return redirect(reverse('forum:list'))

            if not models.LikeComment.objects.filter(user=request.user, comment=comment).exists():
                models.LikeComment.objects.create(user=request.user, comment=comment)
                comment.likes += 1
                comment.user.score += 1
                comment.user.save()
                comment.save()

            if models.Thread.objects.filter(pk=thr_pk).exists():
                return redirect(reverse('forum:details', kwargs={'pk': thr_pk}))

            return redirect(reverse('forum:list'))

        messages.add_message(request,
                             messages.WARNING,
                             f'Login in order to like comment')

        return redirect(reverse('users:login'))


class LikeThreadView(View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            try:
                thread = models.Thread.objects.get(pk=pk)
            except models.Thread.DoesNotExist:
                messages.add_message(request,
                                     messages.WARNING,
                                     f'Thread does not exist')

                return redirect(reverse('forum:list'))

            if not models.LikeThread.objects.filter(user=request.user, thread=thread).exists():
                models.LikeThread.objects.create(user=request.user, thread=thread)
                thread.likes += 1
                thread.creator.score += 1
                thread.creator.save()
                thread.save()

            return redirect(reverse('forum:details', kwargs={'pk': pk}))

        messages.add_message(request,
                             messages.WARNING,
                             f'Login in order to like thread')

        return redirect(reverse('users:login'))
