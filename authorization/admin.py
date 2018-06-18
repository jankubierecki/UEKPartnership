from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.utils.translation import gettext_lazy as _

admin.site.unregister(User)


@admin.register(User)
class SuperuserUserAdmin(UserAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class BasicUser(User):
    class Meta:
        proxy = True
        app_label = "auth"
        verbose_name = "Użytkownik Uczelni"
        verbose_name_plural = "Użytkownicy Uczelni"


@admin.register(BasicUser)
class BasicUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
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
