from django.contrib.auth.mixins import AccessMixin


class CreatorRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        thread = self.get_queryset().get(pk=kwargs.get('pk'))
        if request.user != thread.creator or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
