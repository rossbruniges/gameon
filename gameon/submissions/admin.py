from django.contrib import admin
from gameon.submissions import models


class ChallengeAdmin(admin.ModelAdmin):
    model = models.Challenge
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    prepopulated_fields = {"slug": ("name",)}


class EntryAdmin(admin.ModelAdmin):
    model = models.Entry
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'category', 'created_by', 'award', 'is_grand_champ')
    list_filter = ('category', 'award')
    list_editable = ('award', 'is_grand_champ', )


admin.site.register(models.Challenge, ChallengeAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Entry, EntryAdmin)
