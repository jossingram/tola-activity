import unicodedata
import datetime
import urllib2
import json
import base64

from read.models import Read

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


#IMPORT JSON DATA
def getJSON(id):
    """
    Get JSON feed info from form then grab data
    """
    # retrieve submitted Feed info from database
    read_obj = Read.objects.get(id)
    # set date time stamp
    today = datetime.date.today()
    today.strftime('%Y-%m-%d')
    today = str(today)

    #get auth info from form post then encode and add to the request header
    username = request.POST['user_name']
    password = request.POST['password']
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    request2 = urllib2.Request(read_obj.read_url)
    request2.add_header("Authorization", "Basic %s" % base64string)
    #retrieve JSON data from formhub via auth info
    json_file = urllib2.urlopen(request2)

    #create object from JSON String
    data = json.load(json_file)
    json_file.close()
    #loop over data and insert create and edit dates and append to dict
    row_num = 1
    for row in data:
        for new_label, new_value in row.iteritems():
            if new_value is not "" and new_label is not None:
                #save to DB
                saveData(new_value, new_label, silo_id, row_num)
        row_num = row_num + 1


    return get_fields


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

