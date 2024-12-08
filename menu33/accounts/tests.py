def is_profile_owner(view_instance):
    """
    Ensure the logged-in user can only access their own profile.
    """
    return view_instance.request.user.pk == view_instance.kwargs.get('pk')