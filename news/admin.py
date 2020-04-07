from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from news.forms.group_admin_form import GroupAdminForm
from .models import User, Post, Comment
from .models.custom_group import CustomGroup


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class GroupInline(admin.StackedInline):
    model = CustomGroup
    can_delete = False
    verbose_name_plural = 'pre moderation'


class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupInline,)
    form = GroupAdminForm
    pre_moderation = ['disable_pre_moderation']

    def disable_pre_moderation(self, request, queryset):
        queryset.update(pre_moderation=False)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'status')
    list_filter = ('title', 'author')
    search_fields = ('title',)


admin.site.unregister(Group)

admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
