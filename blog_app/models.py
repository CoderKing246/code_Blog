from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100000)
    created_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,null=True,related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.body[0:20]
    
    
class Profile(models.Model):
    """
    Profile model extending the default User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True, default="profile_images/default.jpg")
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        """
        Override save to provide default behavior for image.
        """
        if not self.image:
            self.image = "profile_images/default.jpg"
        super().save(*args, **kwargs)

# Signal to create or update Profile whenever a User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()