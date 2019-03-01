#
# This file contains high-level configuration variables for CultureMeshFFB.
#
#     DO NOT INCLUDE SENSITIVE CONFIGURATION HERE.  THIS WILL BE
#     IN VERSION CONTROL.
#

import datetime

DEBUG_PORT=8080
DEBUG_ADDR='127.0.0.1'
DATETIME_FMT_STR = "%Y-%m-%d %H:%M:%S"
PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)
