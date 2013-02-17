import os

#assuming the apps with the XML and YAML are both in the same top-level directory as this one
CACHE_DIR = os.path.join(os.getcwd(),'..')
#based on an environment of folders like this:
#--congress
#----dbcongress (this app)
#----congress (from https://github.com/unitedstates/congress, which by running the ./run scripts includes:)
#--------data (various XML and JSON files)
#----congress-legislators (from https://github.com/unitedstates/congress-legislators)
                                        

CONGNO = 113
