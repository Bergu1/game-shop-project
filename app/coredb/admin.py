from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from coredb import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'first_name', 'last_name', 
                    'username', 'email', 'date_of_birth', 'total_balance', 'currency', 'last_login']
    fieldsets = (
        (None, {"fields": ('username', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'username',
                'email',
                'date_of_birth',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'total_balance',
                'currency',
            )
        }),
    )

admin.site.register(models.Person, UserAdmin)

class GamesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'tittle', 'description', 
                    'price', 'image']

admin.site.register(models.Games, GamesAdmin)


class PersonGamesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'person', 'game', 'date']


admin.site.register(models.PersonGames, PersonGamesAdmin)



class AccountHistoryAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'person', 'game', 'date', 'amount']
    

admin.site.register(models.AccountHistory, AccountHistoryAdmin)


class FriendsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'sender', 'recipient', 'status', 'created_at']
    

admin.site.register(models.Friends, FriendsAdmin)


class NewsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'image', 'title', 'content', 'date']
    

admin.site.register(models.News, NewsAdmin)

from django.contrib import admin
from .models import ExchangeRate

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'last_updated')
    actions = ['fetch_exchange_rates']

    def fetch_exchange_rates(self, request, queryset):
        try:
            ExchangeRate.fetch_exchange_rates()
            self.message_user(request, "Curses have been succesfully changed.")
        except Exception as e:
            self.message_user(request, f"Error while download curses: {str(e)}", level="error")

    fetch_exchange_rates.short_description = "Download curses from NBP"