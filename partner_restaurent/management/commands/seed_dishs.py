import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from partner_restaurent import models as partner_models
from users import models as user_models
from faker import Faker
from faker_food import FoodProvider
fake = Faker()
fake.add_provider(FoodProvider)


class Command(BaseCommand):

    help = "This command creates dishs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many dish  you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        restaurent=partner_models.Restaurent.objects.all()
        seeder=Seed.seeder()
        seeder.add_entity(
            partner_models.MenuItem,
            number,
            {
                "name":lambda x:fake.dish(),
                "price":lambda x:random.randint(600,1000),
                "description":lambda x:fake.dish_description(),
                "photo":lambda x:f"dish_photos/{random.randint(1, 35)}.jpeg",
                "restaurent":lambda x:random.choice(restaurent),
                            
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} dishs created!"))