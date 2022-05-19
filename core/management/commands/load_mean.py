from django.core.management.base import BaseCommand
from delivery_man.models import Delivery_mean

class Command(BaseCommand):
    help = 'Load delivery mean'

    def handle(self, *args, **kwargs):
        Delivery_mean.objects.all().delete()
        mean=['velo','voiture','moto']
        if not Delivery_mean.objects.count():
            for item in mean:
                Delivery_mean.objects.create(name=item)
        
       

        
