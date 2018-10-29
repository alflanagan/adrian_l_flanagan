from django.contrib import admin
from navigation.models import Section, Link

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass
