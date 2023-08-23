from rest_framework import serializers
from .models import box

class boxseria(serializers.ModelSerializer):
	class Meta:
		model = box
		fields = ['id','length','breadth','height','area','volume','creator','last_update']