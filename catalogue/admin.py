from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalogue.models import LiteraryFormat, Book, Author


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "format", ]
    list_filter = ["format", ]
    search_fields = ["title", ]


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("pseudonym", )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional information about author:",
         {
             "fields": ("pseudonym",)
         }
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional information about author:",
         {
             "fields": (
                 "first_name",
                 "last_name",
                 "pseudonym",)
         }
        ),
    )

admin.site.register(LiteraryFormat)
