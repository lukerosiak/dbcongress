from django.db import models

# Create your models here.


class Legislator(models.Model):
    
    bioguide = models.CharField(max_length=15, primary_key=True)
    thomas = models.CharField(max_length=15, blank=True, null=True, unique=True)
    govtrack = models.CharField(max_length=15, blank=True, null=True)
    lis = models.CharField(max_length=15, blank=True, null=True)
    opensecrets= models.CharField(max_length=15, blank=True, null=True)
    votesmart= models.CharField(max_length=15, blank=True, null=True)
    icpsr= models.CharField(max_length=15, blank=True, null=True)
    first_name= models.CharField(max_length=63, blank=True, null=True)
    middle_name= models.CharField(max_length=63, blank=True, null=True)
    last_name= models.CharField(max_length=127, blank=True, null=True)
    suffix= models.CharField(max_length=15, blank=True, null=True)
    nickname= models.CharField(max_length=31, blank=True, null=True)
    official_full= models.CharField(max_length=255, blank=True, null=True)
    gender= models.CharField(max_length=1, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, auto_now=False)
    religion= models.CharField(max_length=127, blank=True, null=True)
    
    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)




# include all names here, both alternates and originals...     
class Other_Names(models.Model):
    legislator = models.ForeignKey(Legislator)
    first_name= models.CharField(max_length=63, blank=True, null=True)
    middle_name= models.CharField(max_length=63, blank=True, null=True)
    last_name= models.CharField(max_length=127, blank=True, null=True)
    start = models.DateField(blank=True, null=True, auto_now=False)
    end = models.DateField(blank=True, null=True, auto_now=False)
 
    
class Term(models.Model):
    legislator = models.ForeignKey(Legislator)
    term_type = models.CharField(max_length=15, blank=True, null=True)
    start= models.DateField(blank=True, null=True, auto_now=False)
    end= models.DateField(blank=True, null=True, auto_now=False)
    # Some of these states aren't states, so no US state field. 
    state = models.CharField(max_length=15, blank=True, null=True)
    district = models.CharField(max_length=5, blank=True, null=True)
    term_class = models.CharField(max_length=1, blank=True, null=True)
    party = models.CharField(max_length=63, blank=True, null=True)
    url= models.CharField(max_length=511, blank=True, null=True)
    address = models.CharField(max_length=511, blank=True, null=True)
    
    def __unicode__(self):
        return "%s, %s, %s %s %s %s" % (self.legislator.last_name, self.legislator.first_name, self.party, self.term_type, self.state, self.district)
    
    def chamber(self):
        if self.term_type=='rep':
            return "House"
        elif self.term_type=='sen':
            return "Senate"
        else:
            return self.term_type
            




class Vote(models.Model):
    vote_id = models.TextField(blank=True, primary_key=True)
    category = models.TextField(blank=True)
    chamber = models.TextField(blank=True)
    congress = models.IntegerField(null=True)
    date = models.DateTimeField(null=True, auto_now=False)
    number = models.IntegerField(null=True)
    question = models.TextField(blank=True)
    record_modified = models.DateTimeField(null=True, auto_now=False)
    requires = models.TextField(blank=True)
    result = models.TextField(blank=True)
    result_text = models.TextField(blank=True)
    session = models.TextField(blank=True)
    source_url = models.TextField(blank=True)
    subject = models.TextField(blank=True)
    type = models.TextField(blank=True)
    updated_at = models.DateTimeField(null=True, auto_now=False)

    def __unicode__(self):
        return "%s, %s" % (self.question, self.result)


class VoteCast(models.Model):
    vote = models.ForeignKey(Vote)
    cast = models.TextField(blank=True)
    name = models.TextField(blank=True)
    lsid = models.TextField(blank=True)
    party = models.TextField(blank=True)
    state = models.TextField(blank=True)
    
    
    
    
class Committee(models.Model):
    id = models.TextField(primary_key=True)
    congno = models.IntegerField(blank=True)
    name = models.TextField(blank=True)
    type = models.TextField(blank=True)
    url = models.TextField(blank=True)
    house_committee_id = models.TextField(blank=True)
    senate_committee_id = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
        
class Subcommittee(models.Model):
    id = models.TextField(primary_key=True)
    committee = models.ForeignKey(Committee)
    congno = models.IntegerField(blank=True)
    name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class CommitteeMembership(models.Model):
    committee = models.ForeignKey(Committee)
    bioguide = models.ForeignKey(Legislator)
    congno = models.IntegerField(blank=True)
    name = models.TextField(blank=True)
    party = models.TextField(blank=True)
    rank = models.IntegerField(blank=True)
    thomas = models.TextField(blank=True)
    title = models.TextField(blank=True)

class SubcommitteeMembership(models.Model):
    subcommittee = models.ForeignKey(Subcommittee)
    bioguide = models.ForeignKey(Legislator)
    congno = models.IntegerField(blank=True)
    name = models.TextField(blank=True)
    party = models.TextField(blank=True)
    rank = models.IntegerField(blank=True)
    thomas = models.TextField(blank=True)
    title = models.TextField(blank=True)


