import os

#should automatically be "this directory" + /congress
CACHE_DIR = '/home/luke/research/opencongress/congress'
CACHE_DIR = os.path.join(os.getcwd(),'..','congress')
#based on an environment of folders like this:
#--congress
#----dbcongress (this app)
#----congress (from https://github.com/unitedstates/congress, which by running the ./run scripts includes:)
#--------data (various XML and JSON files)
#--------congress-legislators (also can be cloned directly from https://github.com/unitedstates/congress-legislators)
                                        

CONGNO = 113
