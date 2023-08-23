from django.contrib import admin

# Register your models here.

from .models import box
@admin.register(box)
class boxadmin(admin.ModelAdmin):
	list_display=['length','breadth','height','area','volume','creator','last_update']

	