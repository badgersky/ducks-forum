from django.contrib.auth.mixins import AccessMixin


class ThreadCreatorRequiredMixin(AccessMixin):
    """Verify that the current user is thread creator or admin."""

    def dispatch(self, request, *args, **kwargs):
        thread = self.get_queryset().get(pk=kwargs.get('pk'))
        if request.user != thread.creator and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CommentCreatorRequiredMixin(AccessMixin):
    """Verify that the current user is comment creator or admin."""

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_queryset().get(pk=kwargs.get('pk'))
        if request.user != comment.user and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
