import random
from secrets import choice
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from partner_restaurent import models as partner_models
from users import models as user_models
from core import models as core_models


class Command(BaseCommand):

    help = "This command creates restaurents"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many restaurent do  you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        type_restaurent = partner_models.Type_Resturent.objects.all()
        heur_desponible= core_models.Hour.objects.all()
        jour_desponibilite= core_models.Day.objects.all()
        wilaya=core_models.Wilaya.objects.all()
        commune=core_models.Commune.objects.all()
        seeder.add_entity(
            partner_models.Restaurent_owner,
            number,
        {    'nom':lambda x:seeder.faker.first_name(),
            'prenom':lambda x:seeder.faker.last_name(),}
        )
        res_owners=partner_models.Restaurent_owner.objects.all()
        seeder.add_entity(
            partner_models.Restaurent,
            number,
            {
                'user':lambda x:random.choice(all_users),
                'name':lambda x:seeder.faker.company(),
                'logo':lambda x:f"restaurent_logo/{random.randint(1, 17)}.jpeg",
                'restaurent_owner':lambda x:random.choice(res_owners),
                'address_exacte': lambda x:seeder.faker.address(),
                'type_restaurent': lambda x:random.choice(type_restaurent),
                'heur_debut_desponible': lambda x:seeder.faker.time(),
                'heur_fin_desponible': lambda x:seeder.faker.time(),
                'jour_desponibilite': lambda x:seeder.faker.day_of_week(),
                'mobile':lambda x:seeder.faker.phone_number(),
                'wilaya':lambda x:random.choice(wilaya),
                'commune':lambda x:random.choice(commune),

            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} restaurents created!"))