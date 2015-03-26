import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'putsomethingawesomehere'

DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TIME_ZONE = 'America/Denver'

# In days -- set to 0 if you don't want it
STALE_PERIOD = 7
