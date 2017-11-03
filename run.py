from culturemesh import app
from config import DEBUG_PORT, DEBUG_ADDR

#
# This is the (dev) entry point of the application. 
# Nothing else should be in this file. 
#

if __name__ == "__main__":
	app.run(host=DEBUG_ADDR, port=DEBUG_PORT, debug=True)