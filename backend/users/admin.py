from django.contrib import admin

<<<<<<< HEAD
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "department"]
    list_filter = ["role"]
    search_fields = ["user__username", "department"]
=======
# Register your models here.
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
