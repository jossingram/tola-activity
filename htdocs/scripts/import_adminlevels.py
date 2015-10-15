"""
import json data from API
IMPORTANT!! you must turn off pagination for this to work from a URL and get all
country records
Install module django-extensions
Runs twice via function calls at bottom once
"""
from django.db import connection, transaction

cursor = connection.cursor()
from os.path import exists
import csv
import unicodedata
import sys
import urllib2
from datetime import date
from activitydb.models import Country, Province, District

def run():
    print "Uploading Country Admin data"

getCountry = Country.objects.get(id=4)

def getAllData():

    with open('fixtures/ethipoia_admin_boundaries.csv/Province-Table 1.csv', 'rb') as csvfile:
        country = csv.reader(csvfile, delimiter=',', quotechar='"')
        #check for province and add new ones
        for row in country:
            column_num = 0
            for column in row:
                if column_num == 0:
                    print "Province="
                    print column
                    try:
                        Province.objects.get(name=column, country=getCountry)
                    except Province.DoesNotExist:
                        new_prov = Province(name=column, country=getCountry)
                        new_prov.save()
                    print column
                column_num = column_num + 1

        #check for distrcit and add new one
        for row in country:
            column_num = 0
            new_district = ""
            for column in row:
                if column_num == 0:
                    getProvince = Province.objects.get(name=column, country=getCountry)

                if column_num == 1:
                    print "District="
                    print column
                    new_district = District(name=column, province=getProvince)
                    new_district.save()
                    getProvince = None

                column_num = column_num + 1


getAllData()