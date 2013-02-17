import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import os

from dateutil.parser import parse as dateparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from dbcongress.models import *
from dbcongress.dicttomodel import dictToModel


BASE_DIR = os.path.join(settings.CACHE_DIR,'cache','congress-legislators')
current_committees = os.path.join(BASE_DIR, 'committees-current.yaml')
current_members = os.path.join(BASE_DIR, 'committee-membership-current.yaml')
 
def getmultidict(dictionary, key_list):
    try:
        return reduce(dict.get, key_list, dictionary)
    except TypeError:
        return None



def process_committees():
    y = yaml.load(open(current_committees,'r'),Loader=Loader)
    for committee_yaml in y:
        id = committee_yaml['thomas_id']
        try:
            this_committee = Committee.objects.get(pk=id)
        except Committee.DoesNotExist:
            
            obj = dictToModel(Committee,committee_yaml,pk='thomas_id')
            obj['congno'] = settings.CONGNO
            this_committee = Committee.objects.create(**obj)
            print "Added %s" % (this_committee)
        
        if 'subcommittees' in committee_yaml.keys():
            for subcommittee in committee_yaml['subcommittees']:
                try:
                    subcommittee_id = id + subcommittee['thomas_id']
                    this_subcommittee = Subcommittee.objects.get(pk=subcommittee_id)
                except Subcommittee.DoesNotExist:
                    
                    obj = dictToModel(Subcommittee,subcommittee)
                    obj['pk'] = subcommittee_id
                    obj['committee'] = this_committee
                    obj['congno'] = settings.CONGNO
                    this_subcommittee = Subcommittee.objects.create(**obj)
                    print "Added %s" % (this_subcommittee)
            



def process_members():
    y = yaml.load(open(current_members,'r'),Loader=Loader)
    for committee in y.keys():
        
        if len(committee)<5: #is a main committee

            for membership_yaml in y[committee]:
                
                try:
                    this_membership = CommitteeMembership.objects.get(committee_id=committee,bioguide_id=membership_yaml['bioguide'],congno=settings.CONGNO)
                except CommitteeMembership.DoesNotExist:
                    obj = dictToModel(CommitteeMembership,membership_yaml)
                    obj['committee_id'] = committee
                    obj['congno'] = settings.CONGNO
                    obj['bioguide_id'] = membership_yaml['bioguide']
                    CommitteeMembership.objects.create(**obj)
                    

        else: #subcommittee
        
            for membership_yaml in y[committee]:
                
                try:
                    this_membership = SubcommitteeMembership.objects.get(subcommittee_id=committee,bioguide_id=membership_yaml['bioguide'],congno=settings.CONGNO)
                except SubcommitteeMembership.DoesNotExist:
                    obj = dictToModel(SubcommitteeMembership,membership_yaml)
                    obj['subcommittee_id'] = committee
                    obj['congno'] = settings.CONGNO
                    obj['bioguide_id'] = membership_yaml['bioguide']
                    SubcommitteeMembership.objects.create(**obj)
                    

               
         
class Command(BaseCommand):
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        process_committees()
        process_members()
