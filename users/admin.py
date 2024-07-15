from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "avatar",
        "phone_number",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("phone_number", "first_name", "last_name")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    exclude = ("content_id", "user")
    search_fields = ("user",)
