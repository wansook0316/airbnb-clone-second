from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import Facility


class Command(BaseCommand):

    # 해당 py file이 어떤 역할을 하는지에 대한 설명
    help = "This command creates Facilities"

    # 해당 python 의 arg를 추가해준다. 이 경우는 필요없다.
    """
    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that i love you"
        )
    """

    # arg에 따라 실행해줄 동작을 정의한다.
    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))
