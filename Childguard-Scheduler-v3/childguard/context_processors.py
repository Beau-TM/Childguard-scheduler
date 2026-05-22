from .models import Problem


def unread_count(request):
    """Make unread_count available in all templates for admin users."""
    if request.user.is_authenticated and request.user.is_admin_or_director():
        return {'unread_count': Problem.objects.filter(is_new=True).count()}
    return {'unread_count': 0}
