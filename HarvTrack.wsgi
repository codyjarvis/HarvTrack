import sys, os

sys.path.insert(0,'/var/www/HarvTrack')
os.chdir('/var/www/HarvTrack')
from HarvTrack import app as application
