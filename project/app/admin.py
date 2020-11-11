from django.contrib import admin
from .models import *
from embed_video.admin import AdminVideoMixin


admin.site.site_header = "Legacy News"
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(TeamInfo)
admin.site.register(Contact)
admin.site.register(Images)
admin.site.register(FooterLinks)
admin.site.register(HomepageAboutText)
