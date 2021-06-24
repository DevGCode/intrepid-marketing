from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostView)
admin.site.register(WebsiteAudit)
admin.site.register(Service)

# Marketing
admin.site.register(Signup)

