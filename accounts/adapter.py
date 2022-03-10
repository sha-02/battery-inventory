'''
Disable new users singup when using Django's allauth package

https://stackoverflow.com/questions/29794052/how-could-one-disable-new-account-creation-with-django-allauth-but-still-allow
https://simpleit.rocks/python/django/disable-new-users-signup-in-django-allauth/
'''

from allauth.account.adapter import DefaultAccountAdapter


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    """
    Adapter to disable allauth new signups

    https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-redirects """

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        """
        return False

'''
Then add the bellow setting in settings.py:

ACCOUNT_ADAPTER = 'accounts.adapter.NoNewUsersAccountAdapter'
'''