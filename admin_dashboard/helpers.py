import random
from .services import load_state,load_local_govt
from .models import (State,
                    LocalGovt,
                    Country,ProductStatus,ProductType)
from .contants import COUNTRY
from .models import ProductTag
from .contants import TAG,PRODUCT_TYPE,PROPERTY_STATUS


def createCountry():
    try:
        for country in COUNTRY:
            obj,created=Country.objects.get_or_create(
                name=country,
                defaults={
                    "name":country
                }
            )
            fetch_state(obj)
    except Exception as e:
        return None

def fetch_state(country:Country):
    try:
        for state in load_state():
            obj,created=State.objects\
                .update_or_create(name=state,defaults={"name":state,"country":country})
            fetch_local_govt(obj)
    except Exception as e:
        return None
       
def fetch_local_govt(state):
    try:
        for lga in load_local_govt(state):
            LocalGovt.objects.get_or_create(
                LGA=lga,
                defaults={
                    "state":state,
                    "LGA":lga
                }
            )
    except Exception as e:
        return None
    

def loadProductTag():
    for tag in TAG:
        ProductTag.objects.get_or_create(
            name=tag,
            defaults={
                "name":tag
            }
        )


def loadProductStatus():
    for tag in PROPERTY_STATUS:
        ProductStatus.objects.get_or_create(
            name=tag,
            defaults={
                "name":tag
            }
        )


def loadProductType():
    for tag in PRODUCT_TYPE:
        ProductType.objects.get_or_create(
            name=tag,
            defaults={
                "name":tag
            }
        )