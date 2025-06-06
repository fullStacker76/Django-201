from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

# Create your models here.
class Profile (models.Model):
    user = models.OneToOneField(
        User,
        on_delete= models.CASCADE,
        related_name= 'profile'
    )
    image = ImageField(upload_to='profiles', default='default.jpg')
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)    
def create_user_profile(sender, instance, created, **kwargs):
    # Create new Profile object when User is created
    if created:
        Profile.objects.create(user=instance)