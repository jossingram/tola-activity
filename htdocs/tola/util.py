import unicodedata
import datetime
import urllib2
import json
import base64

from djangocosign.models import UserProfile, Country
from activitydb.models import Country as ActivityCountry

#CREATE NEW DATA DICTIONARY OBJECT 
def siloToDict(silo):
    parsed_data = {}
    key_value = 1
    for d in silo:
        label = unicodedata.normalize('NFKD', d.field.name).encode('ascii','ignore')
        value = unicodedata.normalize('NFKD', d.char_store).encode('ascii','ignore')
        row = unicodedata.normalize('NFKD', d.row_number).encode('ascii','ignore')
        parsed_data[key_value] = {label : value}

        key_value += 1

    return parsed_data


def getCountry(user):
        """
        Returns the object the view is displaying.

        """
        # get users country from django cosign module
        user_countries = UserProfile.objects.all().filter(user=user).values('countries')
        # get the country name from django cosign module
        get_cosign_country = Country.objects.all().filter(id__in=user_countries).values('name')
        # get the id from the activitydb model
        get_countries = ActivityCountry.objects.all().filter(country__in=get_cosign_country)

        return get_countries

