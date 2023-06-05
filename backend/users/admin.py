from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'who',
        'first_name',
        'last_name',
        'role',
    )
    fieldsets = (
        ('Данные пользователя', {
            'fields': ('username', 'first_name', 'last_name')
        }),
        ('Идентификатор', {'fields': ('who',)}),
        ('Пользовательская роль и статус', {'fields': ('role', 'status')}),
    )
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'
