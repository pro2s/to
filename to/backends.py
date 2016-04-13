from django.contrib.auth.models import User
import sys
import ldap

def check_credentials(username, password):
        
        """Verifies credentials for username and password.
        Returns None on success or a string describing the error on failure
        # Adapt to your needs
        """
        LDAP_SERVER = 'ldap://10.1.0.50'
        # fully qualified AD user name
        LDAP_USERNAME = '%s@elmotor.org' % username
        # your password
        LDAP_PASSWORD = password
        base_dn = 'DC=elmotor,DC=org'
        ldap_filter = 'userPrincipalName=%s@elmotor.org' % username
        attrs = ['memberOf']
        try:
            # build a client
            ldap_client = ldap.initialize(LDAP_SERVER)
            # perform a synchronous bind
            ldap_client.set_option(ldap.OPT_REFERRALS,0)
            ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            return 'Wrong username or password'
        except ldap.SERVER_DOWN:
            return 'AD server not awailable'
        # all is well
        ldap_client.unbind()
        return None
        
class TasksBackend(object):
    def authenticate(self, username=None, password=None):
        pwd_valid = check_credentials(username, password)
        if pwd_valid is None:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='*')
                user.is_staff = True
                user.is_active = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        print "get_user"
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None