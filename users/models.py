import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import uuid
from django.conf import settings


# Create your models here.

class User(AbstractUser):
    #this one is for profile picture
    avatar = models.ImageField(upload_to="user_avatars", blank=True)
    # address=models.CharField(max_length=50,blank=True)
    is_delivery_man=models.BooleanField(default=False)
    is_partner=models.BooleanField(default=False)
    email_confirmed=models.BooleanField(default=False)
    email_pass=models.CharField(max_length=130,default="",blank=True)
     #this is a general function to verify email
    
    def verify_email(self):
        if self.email_confirmed is False:
            secret = uuid.uuid4().hex[:20]
            self.email_pass = secret
            html_message = render_to_string(
                "email/email_verify.html", {"secret": secret}
            )
            send_mail(
                ("Verify OrderIt Account"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
