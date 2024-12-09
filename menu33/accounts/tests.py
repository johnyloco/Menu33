from django.shortcuts import get_object_or_404

from menu33.accounts.models import Profile


def is_profile_owner(view_instance):
    profile = get_object_or_404(Profile, pk=view_instance.kwargs['pk'])
    return view_instance.request.user == profile.user