import json
import os

from dateutil.parser import parse as dateparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from dbcongress.models import *
from dbcongress.dicttomodel import dictToModel

 
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))




        

def process_file(congno):

    BASE_DIR = os.path.join(settings.CACHE_DIR,'data',"%s"%congno,'bills')
    os.chdir(BASE_DIR)
    for year in os.listdir('.'):
        os.chdir(os.path.join(BASE_DIR,year))
        for bill in os.listdir('.'):
            os.chdir(os.path.join(BASE_DIR,year,bill))
            jfile = removeNonAscii(open('data.json','r').read())
            j = json.loads(jfile)

            if not Bill.objects.filter(pk=j['bill_id']).count():
                bill = Bill.objects.create(**dictToModel(Bill,j))
                    
                for cosponsor in j['cosponsors']:

                    bill.cosponsor_set.create( **dictToModel(Cosponsor,cosponsor) )


class Command(BaseCommand):
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        process_file(settings.CONGNO)


