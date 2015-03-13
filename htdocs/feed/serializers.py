from django.forms import widgets
from rest_framework import serializers
from read.models import Read, ReadType
from silo.models import ValueStore, Silo, DataField
from django.contrib.auth.models import User


class SiloSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Silo
        fields = ('owner', 'name', 'source', 'description', 'create_date', 'id')
        depth =1


class DataFieldSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DataField
        fields = ('silo', 'name', 'is_uid', 'create_date', 'edit_date')
        depth=1


class ValueStoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ValueStore
        fields = ('field', 'char_store', 'create_date', 'edit_date')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ReadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Read
        fields = ('owner', 'type', 'read_name', 'read_url')


class ReadTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReadType
        fields = ( 'type', 'description')
