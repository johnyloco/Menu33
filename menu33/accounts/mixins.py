from django.http import HttpResponseForbidden


class CustomPermissionMixin:
    def handle_no_permission(self):
        """
        Customize the behavior when the user fails the test_func check.
        """
        return HttpResponseForbidden("You do not have permission to perform this action.")
