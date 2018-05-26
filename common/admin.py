from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


class ReadOnlyModelAdmin(object):
    """
    ModelAdmin class that prevents modifications through the admin.
    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    Source: https://gist.github.com/aaugustin/1388243
    """

    def get_actions(self, request):
        if request.user.is_superuser:
            return super(ReadOnlyModelAdmin, self).get_actions(request)
        else:
            return None

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and self.has_only_view_permission(request, obj):
            if not self.fields:
                raise ValueError("`fields` field has to be set!")
            return self.fields
        return super(ReadOnlyModelAdmin, self).get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return self.is_request_safe(request) or super().has_change_permission(request, obj)
        return (self.is_request_safe(request)
                and self.has_only_view_permission(request, obj)) \
               or super().has_change_permission(request, obj)

    def is_request_safe(self, request):
        return request.method in ['GET', 'HEAD']

    def has_only_view_permission(self, request, obj):
        content_type = ContentType.objects.get_for_model(obj)
        user: User = request.user
        view_permission = "%s.view_%s" % (content_type.app_label, content_type.model)
        change_permission = "%s.change_%s" % (content_type.app_label, content_type.model)
        add_permission = "%s.add_%s" % (content_type.app_label, content_type.model)
        delete_permission = "%s.delete_%s" % (content_type.app_label, content_type.model)
        return user.has_perm(view_permission) and not user.has_perm(change_permission) and not user.has_perm(
            add_permission) and not user.has_perm(delete_permission)
