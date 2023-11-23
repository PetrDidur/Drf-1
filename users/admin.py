from django.contrib import admin

from users.models import User


@admin.register(User)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'avatar', 'role',)

