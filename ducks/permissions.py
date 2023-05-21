from django.contrib.auth.mixins import AccessMixin


class DuckCreatorRequiredMixin(AccessMixin):
    """Verify that the current user is duck creator or admin"""

    def dispatch(self, request, *args, **kwargs):
        duck = self.get_queryset().get(pk=kwargs.get('pk'))
        if request.user != duck.user and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
