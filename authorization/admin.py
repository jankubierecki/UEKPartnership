from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from authorization.models import User, BasicUser


class BaseUserAdmin(UserAdmin):
    """ Users """

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')


@admin.register(User)
class SuperuserUserAdmin(BaseUserAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(BasicUser)
class BasicUserAdmin(BaseUserAdmin):
    """ University Users """

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(BasicUserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["first_name"].required = True
        form.base_fields["first_name"].widget.is_required = True
        form.base_fields["last_name"].required = True
        form.base_fields["last_name"].widget.is_required = True
        form.base_fields["email"].required = True
        form.base_fields["email"].widget.is_required = True

        return form

    def get_queryset(self, request):
        return BasicUser.objects.filter(
            is_superuser=False
        )

    def save_model(self, request, obj: BasicUser, form, change):
        obj.is_staff = True
        with transaction.atomic():
            super(BasicUserAdmin, self).save_model(request, obj, form, change)
            group, _ = Group.objects.get_or_create(
                name="Przeglądający"
            )
            group.user_set.add(obj)
            group.save()
        return obj
