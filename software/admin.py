# pylint: disable=missing-docstring
from django.contrib import admin
from software.models import SoftwareProject, Category, TechUsed, SoftwareTechUsed

@admin.register(SoftwareProject)
class SoftwareProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(TechUsed)
class TechUsedAdmin(admin.ModelAdmin):
    pass

@admin.register(SoftwareTechUsed)
class SoftwareTechUsedAdmin(admin.ModelAdmin):
    pass
