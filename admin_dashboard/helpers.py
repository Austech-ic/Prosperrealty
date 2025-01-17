import calendar
import random
from .services import load_state,load_local_govt
from .models import (State,
                    LocalGovt,
                    Country,ProductStatus,ProductType,Visitors)
from .contants import COUNTRY
from .models import ProductTag
from .contants import TAG,PRODUCT_TYPE,PROPERTY_STATUS
from django.utils.timezone import now

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


def get_analytics(year) -> list:
    """Returns the monthly analytics of the invoices passed as parameter"""
    result = [
        {
            "month": calendar.month_abbr[month_no],
            "point":Visitors.objects.filter(
                month=calendar.month_abbr[month_no],
                year=str(year)
            ).first().count
            if Visitors.objects.filter(
                month=calendar.month_abbr[month_no],
                year=str(year)
            ).first()
            else int(0),
        }
        for month_no in range(1, 13)
    ]

    return result