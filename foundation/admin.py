from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import *

class AdminVideo(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Payment)
admin.site.register(Blog)
admin.site.register(Contact)
admin.site.register(Event)
admin.site.register(HomeBlog)
admin.site.register(HomeEvent)
admin.site.register(LatestCause)
admin.site.register(Comment)
admin.site.register(YouTube, AdminVideo)


class GallryInLine(admin.TabularInline):
    model = MyGallery
    extra = 3
    
  
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 'image', 'slug']})]
    inlines = [GallryInLine]
    prepopulated_fields = {"slug": ("name",)}
  
  
admin.site.register(MyCategory, CategoryAdmin)