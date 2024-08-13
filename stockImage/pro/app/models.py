from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class extended(models.Model):
    id = models.OneToOneField (User,primary_key = True, on_delete = models.CASCADE)
    img = models.ImageField()
    class Meta:
        app_label = 'app'
        db_table = 'app_extended'
    def __str__(self):
        return str(self.id)

class StockImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stock_images/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title