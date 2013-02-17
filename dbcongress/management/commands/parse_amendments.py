import json
import os

from dateutil.parser import parse as dateparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from dbcongress.models import *
from dbcongress.dicttomodel import dictToModel

 
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))




        

def process_file(congno):

    BASE_DIR = os.path.join(settings.CACHE_DIR,'congress','data',"%s"%congno,'amendments')
    os.chdir(BASE_DIR)
    for year in os.listdir('.'):
        os.chdir(os.path.join(BASE_DIR,year))
        for bill in os.listdir('.'):
            os.chdir(os.path.join(BASE_DIR,year,bill))
            jfile = removeNonAscii(open('data.json','r').read())
            j = json.loads(jfile)

            if not Amendment.objects.filter(pk=j['amendment_id']).count():
                obj = dictToModel(Amendment,j)
                print obj
                amends_type = j['amends'][ "%s_type" % j['amends']['document_type'] ]
                obj['amends_id'] = "%s%s-%s" % (amends_type,j['amends']['number'],j['amends']['congress'])
                amendment = Amendment.objects.create(**obj)
                    
                #actions: for cosponsor in j['cosponsors']:
                #    bill.cosponsor_set.create( **dictToModel(Cosponsor,cosponsor) )




class Command(BaseCommand):
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        process_file(settings.CONGNO)


