from django.db import connection

from .models import Company


class CompanyService:
    @staticmethod
    def get_or_create_company(data):
        name = data.get('name')
        logo = data.get('logo')
        company, created = Company.objects.get_or_create(name=name, defaults={'logo': logo})

        if company.logo != logo:
            company.logo = logo
            company.save(update_fields=['logo'])
        return company
