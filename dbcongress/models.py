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
    
    class Meta:
        unique_together = (("vote", "lsid"),)
    
    
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

    #class Meta:
    #    unique_together = (("vote", "lsid"),)


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

    class Meta:
        unique_together = (("committee", "bioguide", "congno"),)


class SubcommitteeMembership(models.Model):
    subcommittee = models.ForeignKey(Subcommittee)
    bioguide = models.ForeignKey(Legislator)
    congno = models.IntegerField(blank=True)
    name = models.TextField(blank=True)
    party = models.TextField(blank=True)
    rank = models.IntegerField(blank=True)
    thomas = models.TextField(blank=True)
    title = models.TextField(blank=True)

    class Meta:
        unique_together = (("subcommittee", "bioguide", "congno"),)





#amendment

class Bill(models.Model):
    bill_id = models.TextField(primary_key=True)
    bill_type = models.TextField(blank=True)
    congno = models.IntegerField(blank=True,verbose_name="congress")
    introduced_at = models.DateTimeField(null=True)
    number = models.TextField(blank=True)
    official_title = models.TextField(blank=True)
    popular_title = models.TextField(blank=True)
    short_title = models.TextField(blank=True)
    status = models.TextField(blank=True)
    status_at = models.DateTimeField(null=True)

    awaiting_signature = models.BooleanField(blank=True,verbose_name="history__awaiting_signature")
    enacted = models.BooleanField(blank=True,verbose_name="history__enacted")
    vetoed = models.BooleanField(blank=True,verbose_name="history__vetoed")

    sponsor_thomas_id = models.TextField(blank=True,verbose_name="sponsor__thomas_id")
    sponsor_name = models.TextField(blank=True,verbose_name="sponsor__name")
    sponsor_type = models.TextField(blank=True,verbose_name="sponsor__type")


class Cosponsor(models.Model):
    bill = models.ForeignKey(Bill)
    thomas_id = models.TextField(blank=True)
    name = models.TextField(blank=True)
    sponsored_at = models.DateField(null=True)
    withdrawn_at = models.DateField(null=True)





"""
{
  "actions": [
    {
      "acted_at": "2013-01-22", 
      "committee": "Committee on Commerce, Science, and Transportation", 
      "references": [
        {
          "reference": "CR S44-45", 
          "type": "text of measure as introduced"
        }
      ], 
      "status": "REFERRED", 
      "text": "Read twice and referred to the Committee on Commerce, Science, and Transportation.", 
      "type": "referral"
    }
  ], 
  "amendments": [], 
  "bill_id": "s4-113", #ok
  "bill_type": "s", #ok
  "committees": [
    {
      "activity": [
        "referral", 
        "in committee"
      ], 
      "committee": "Senate Commerce, Science, and Transportation", 
      "committee_id": "SSCM"
    }
  ], 
  "congress": "113", #ok
  "cosponsors": [
    {
      "district": null, 
      "name": "Wyden, Ron", 
      "sponsored_at": "2013-01-22", 
      "state": "OR", 
      "thomas_id": "01247", 
      "title": "Sen", 
      "withdrawn_at": null
    }
  ], 
  "enacted_as": null, 
  "history": {
    "awaiting_signature": false, 
    "enacted": false, 
    "vetoed": false
  }, 
  "introduced_at": "2013-01-22", #ok
  "number": "4", #ok
  "official_title": "A bill to create jobs and strengthen our economy by rebuilding our Nation's infrastructure.", #ok
  "popular_title": null, #ok
  "related_bills": [], 
  "short_title": "Rebuild America Act",#ok 
  "sponsor": {
    "district": null, 
    "name": "Reid, Harry", 
    "state": "NV", 
    "thomas_id": "00952", 
    "title": "Sen", 
    "type": "person"
  }, 
  "status": "REFERRED", #ok
  "status_at": "2013-01-22", #ok
  "subjects": [
    "Academic performance and assessments", 
    "Advanced technology and technological innovations", 
    "Alternative and renewable resources", 
    "Atmospheric science and weather", 
    "Dams and canals", 
    "Economics and public finance", 
    "Education programs funding", 
    "Educational facilities and institutions", 
    "Electric power generation and transmission", 
    "Elementary and secondary education", 
    "Employee hiring", 
    "Energy efficiency and conservation", 
    "Environmental health", 
    "Environmental technology", 
    "Floods and storm protection", 
    "Higher education", 
    "Income tax credits", 
    "Income tax deductions", 
    "Infrastructure development", 
    "Internet and video services", 
    "Natural disasters", 
    "Navigation, waterways, harbors", 
    "Oil and gas", 
    "Public-private cooperation", 
    "Railroads", 
    "Transportation programs funding", 
    "Water quality", 
    "Water resources funding", 
    "Water use and supply"
  ], 
  "subjects_top_term": "Economics and public finance", 
  "summary": {
    "as": "Introduced", 
    "date": "2013-01-22", 
    "text": "Rebuild America Act - Expresses the sense of the Senate that Congress should: create jobs and support businesses while improving the nation's global competitiveness by modernizing and strengthening our national infrastructure; invest resources in transportation corridors that promote commerce and reduce congestion; update and enhance the U.S. network of rail, dams, and ports; develop innovative financing mechanisms for infrastructure to leverage federal funds with private sector partners; invest in critical infrastructure to reduce energy waste and bolster investment in clean energy jobs and industries; invest in clean energy technologies that help free the United States from its dependence on oil; eliminate wasteful tax subsidies that promote pollution and fail to reduce our reliance on foreign oil; spur innovation by facilitating the development of new cutting-edge broadband internet technology and improving internet access for all Americans; modernize, renovate, and repair elementary and secondary school buildings in order to support improved educational outcomes; invest in the nation's crumbling water infrastructure to protect public health and reduce pollution; upgrade and repair the nation's system of flood protection infrastructure to protect public safety; and invest in U.S. infrastructure to address vulnerabilities to natural disasters and the impacts of extreme weather."
  }, 
  "titles": [
    {
      "as": "introduced", 
      "title": "Rebuild America Act", 
      "type": "short"
    }, 
    {
      "as": "introduced", 
      "title": "A bill to create jobs and strengthen our economy by rebuilding our Nation's infrastructure.", 
      "type": "official"
    }
  ], 
  "updated_at": "2013-02-16T04:17:49-05:00"
}"""
