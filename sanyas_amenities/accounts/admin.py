from django.contrib import admin
from django import forms

from .models import User


class UserAdminForm(forms.ModelForm):
    labels = 'Описание'

    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = (
        'id', 'email', 'first_name', 'second_name', 'phone', 'staff', 'admin', 'is_active'
    )
    list_display_links = ('id', 'email')
    search_fields = ('email', 'phone')
    list_filter = ('staff', 'admin', 'is_active')
    fields = (
        'email', 'first_name', 'second_name', 'phone', 'staff', 'admin'
    )
    readonly_fields = ('is_active', 'timestamp')
    save_on_top = True


admin.site.register(User, UserAdmin)
