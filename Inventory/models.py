from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

class box(models.Model):
	length = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
	breadth = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
	height = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	last_update = models.DateTimeField(auto_now=True)


	@property
	def area(self):
		return self.length*self.breadth

	@property
	def volume(self):
		return self.length*self.breadth*self.height
