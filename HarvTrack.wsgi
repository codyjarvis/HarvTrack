import sys, os

sys.path.insert(0,'/var/www/TimeAndTemp')
os.chdir('/var/www/TimeAndTemp')
from TimeAndTemp import app as application
