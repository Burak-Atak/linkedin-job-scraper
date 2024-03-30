from .models import City


class CityService:
    @staticmethod
    def get_or_create_city(name):
        city, created = City.objects.get_or_create(name=name)

        return city
