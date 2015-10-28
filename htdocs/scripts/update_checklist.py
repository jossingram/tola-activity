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
from activitydb.models import ProjectAgreement, Checklist, ChecklistItem

def run():
    print "Uploading Country Admin data"


def getAllData():

    getProjects = ProjectAgreement.objects.all()
    for item in getProjects:
            try:
                Checklist.objects.get(agreement=item)
            except Checklist.DoesNotExist:
                new_checklist = Checklist(agreement=item)
                new_checklist.save()

                get_checklist = Checklist.objects.get(id=new_checklist.id)
                get_globals = ChecklistItem.objects.all().filter(global_item=True)
                for item in get_globals:
                    ChecklistItem.objects.create(checklist=get_checklist,item=item.item)
            print item


getAllData()