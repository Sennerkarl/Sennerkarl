from .models import Data


countries = sorted(list(Data.objects.values_list('country', flat=True).distinct()))


def grabcountries(*args):
    return {'allcountries':countries}




