import json
import os

from dateutil.parser import parse as dateparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from dbcongress.models import *
from dbcongress.dicttomodel import dictToModel

 
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

        

def process_file(congno):

    BASE_DIR = os.path.join(settings.CACHE_DIR,'congress','data',"%s" % congno,'votes')
    os.chdir(BASE_DIR)
    for year in os.listdir('.'):
        os.chdir(os.path.join(BASE_DIR,year))
        for bill in os.listdir('.'):
            os.chdir(os.path.join(BASE_DIR,year,bill))
            jfile = removeNonAscii(open('data.json','r').read())
            j = json.loads(jfile)

            if not Vote.objects.filter(pk=j['vote_id']).count():
                vote = Vote.objects.create(**dictToModel(Vote,j))
                    
                for key in j['votes'].keys():
                    for member in j['votes'][key]:

                        vote.votecast_set.add( VoteCast(cast=key, name=removeNonAscii(member["display_name"]), lsid=member["id"],
                            party=member["party"], state=member["state"])
                            )


class Command(BaseCommand):
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        process_file(settings.CONGNO)


"""
missed votes query:
SELECT congress.votes.chamber, congress.votes_members.lsid, CONCAT(EXTRACT(Year FROM date), EXTRACT(Month FROM date)) AS m, congress.votes_members.name, 
Sum(case WHEN vote_cast='Not Voting' THEN 1 ELSE 0 END) AS missed, Count(congress.votes_members.vote_id) AS n, 
Sum(CASE WHEN vote_cast='Not Voting' THEN 1 ELSE 0 END)/Count(congress.votes_members.vote_id) AS pct
FROM congress.votes INNER JOIN congress.votes_members ON congress.votes.vote_id = congress.votes_members.vote_id
GROUP BY congress.votes.chamber, congress.votes_members.lsid, CONCAT(EXTRACT(year FROM date), EXTRACT(Month FROM date)), congress.votes_members.name
ORDER BY Sum(CASE WHEN vote_cast='Not Voting' THEN 1 ELSE 0 END)*100/Count(congress.votes_members.vote_id) DESC;
"""
