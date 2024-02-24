from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Register your models here.
User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "is_active", "belong_groups")

    # 编辑资料的时候显示的字段
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        # (_('Personal info'), {'fields': ('phone', 'first_name', 'last_name', 'email')}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )
    # 新增用户需要填写的字段
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )
    filter_horizontal = ("groups",)

    @admin.display(description="所属分组")
    def belong_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
