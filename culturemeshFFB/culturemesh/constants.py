"""
Constants needed at the top-level site or by more than
one blueprint.
"""

BLANK_PROFILE_IMG_URL = "https://www.culturemesh.com/images/cm_logo_blank_profile_lrg.png#"
USER_IMG_URL_FMT = "https://www.culturemesh.com/user_images/%s"

#### Messages ####
LOGIN_FAILED_MSG = "Login failed, try again"
LOGIN_MSG = "Sign in to find your diaspora"
LOGIN_ERROR = "You must input a password and a username"

REGISTER_MSG = "Register for a CultureMesh account"
REGISTER_PASSWORDS_DONT_MATCH_MSG = "The passwords you entered do not match.  Try again"
REGISTER_ERROR_MSG = "There was an error processing your form.  Did you leave a field blank by accident?"
REGISTER_USERNAME_TAKEN_MSG = "Oops!  That username is already taken.  Try another one."
REGISTER_UPSTREAM_ERROR_MSG = "That username or email is taken.  Try another combination."
PRIVACY_MSG = "* Only your first name and your username will be publicly visible."

# TODO: implement password resets.
REGISTER_EMAIL_TAKEN_MSG = "Oops!  Looks that email already belongs to an account."
