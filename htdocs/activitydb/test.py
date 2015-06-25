from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from activitydb.models import Program, Country, Province, Village, District, ProjectAgreement, ProjectComplete, Community, Office, Documentation, Monitor, Benchmarks, TrainingAttendance, Beneficiary, Budget
from activitydb.views import CommunityUpdate

class CommunityTestCase(TestCase):

    fixtures = ['/fixtures/country.json','/fixtures/province.json','/fixtures/district.json','/fixtures/district.json','/fixtures/profile_type.json']

    """
    name = models.CharField("Profile Name", max_length=255, blank=True, null=True)
    type = models.ForeignKey(ProfileType, blank=True, null=True)
    office = models.ForeignKey(Office, default="1")
    existing_village = models.BooleanField("Is There an existing shura or CDC?", default="False")
    existing_village_descr = models.CharField("If Yes please describe", max_length=255, blank=True, null=True)
    community_leader = models.CharField("Community Malik/Elder Name", max_length=255, blank=True, null=True)
    head_of_institution = models.CharField("Head of Shura/Institution", max_length=255, blank=True, null=True)
    date_of_firstcontact = models.DateTimeField(null=True, blank=True)
    contact_number = models.CharField("Head of Shura/Institution", max_length=255, blank=True, null=True)
    num_members = models.CharField("Number of Members", max_length=255, blank=True, null=True)
    distance_district_capital = models.IntegerField("Distance from District Capital", help_text="In KM", null=True, blank=True)
    distance_site_camp = models.IntegerField("Distance from Site Camp", help_text="In KM", null=True, blank=True)
    distance_field_office = models.IntegerField("Distance from MC Field Office", help_text="In KM", null=True, blank=True)
    total_num_households = models.IntegerField("Total # Households", help_text="", null=True, blank=True)
    avg_household_size = models.DecimalField("Average Household Size", decimal_places=14,max_digits=25, null=True, blank=True)
    male_0_14 = models.IntegerField("Male age 0-14", null=True, blank=True)
    female_0_14 = models.IntegerField("Female age 0-14", null=True, blank=True)
    male_15_24 = models.IntegerField("Male age 15-24 ", null=True, blank=True)
    female_15_24 = models.IntegerField("Female age 15-24", null=True, blank=True)
    male_25_59 = models.IntegerField("Male age 25-59", null=True, blank=True)
    female_25_59 = models.IntegerField("Female age 25-59", null=True, blank=True)
    male_over_60 = models.IntegerField("Male Over 60", null=True, blank=True)
    female_over_60 = models.IntegerField("Female Over 60", null=True, blank=True)
    total_population = models.IntegerField(null=True, blank=True)
    total_land = models.IntegerField("Total Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_agricultural_land = models.IntegerField("Total Agricultural Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_rainfed_land = models.IntegerField("Total Rain-fed Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_horticultural_land = models.IntegerField("Total Horticultural Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_literate_peoples = models.IntegerField("Total Literate People", help_text="", null=True, blank=True)
    literate_males = models.IntegerField("Number of Literate Males", help_text="", null=True, blank=True)
    literate_females = models.IntegerField("Number of Literate Females", help_text="", null=True, blank=True)
    literacy_rate = models.IntegerField("Literacy Rate (%)", help_text="", null=True, blank=True)
    population_owning_land = models.IntegerField("Population Owning Land", help_text="(%)", null=True, blank=True)
    avg_landholding_size = models.IntegerField("Average Landholding Size", help_text="In hectares/jeribs", null=True, blank=True)
    population_owning_livestock = models.IntegerField("Population Owning Livestock", help_text="(%)", null=True, blank=True)
    animal_type = models.CharField("Animal Types", help_text="See Guide for Calculation", max_length=255, null=True, blank=True)
    num_animals_population_owning = models.CharField(help_text="What?", max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country)
    province = models.ForeignKey(Province, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True)
    village = models.CharField("Village", help_text="", max_length=255, null=True, blank=True)
    latitude = models.DecimalField("Latitude (Coordinates)", decimal_places=14,max_digits=25, blank=True, null=True)
    longitude = models.DecimalField("Longitude (Coordinates)", decimal_places=14,max_digits=25, blank=True, null=True)
    approval = models.CharField("Approval", default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,help_text='This is the Provincial Line Manager', blank=True, null=True, related_name="comm_approving")
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='This is the originator', blank=True, null=True, related_name="comm_estimate")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    """

    def setUp(self):
        new_country = Country.objects.create(country="testcountry")
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_province = Province.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = Province.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice",province=new_province)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        new_community = Community.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()


    def test_community_exists(self):
        """Check for Community object"""
        get_community = Community.objects.get(name="testcommunity")
        self.assertEqual(Community.objects.filter(id=get_community.id).count(), 1)