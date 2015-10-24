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
from activitydb.models import ProjectAgreement, Checklist

def run():
    print "Uploading Country Admin data"


def getAllData():

    getProjects = ProjectAgreement.objects.all()
    for item in getProjects:
            try:
                Checklist.objects.get(agreement=item)
            except Checklist.DoesNotExist:
                new_checklist = Checklist(agreement=item,in_file=False,not_applicable=False)
                new_checklist.save()
            print item


getAllData()