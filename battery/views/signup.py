from allauth.account.views import SignupView
from battery.models import BatteryType, BatteryModel

# Override the django-allauth SignupView to add a set of pre-defined BatteryType and BatteryModel when a new user
#  is created
#  https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/
#  https://django-allauth.readthedocs.io/en/latest/views.html#signup-account-signup


class AccountSignupView(SignupView):
    # Extend Django allauth Signup View to create pre-defined battery types and models for each new user

    # change template's name and path
    # template_name = "users/custom_signup.html"

    # You can also override some other methods of SignupView
    # Like below:
    # def form_valid(self, form):
    #     ...
    #
    # def get_context_data(self, **kwargs):
    #     ...
    def form_valid(self, form):
        # Call the parent's form_valid method
        ret = SignupView.form_valid(self, form)

        # Create pre-defined battery types for the new user
        BatteryType(type='AA', description='', user=self.user).save()
        BatteryType(type='AAA', description='', user=self.user).save()

        # Create pre-defined battery models for the new user
        BatteryModel(description='Non-Rechargeable', user=self.user).save()
        BatteryModel(description='Rechargeable 1.2V', user=self.user).save()
        BatteryModel(description='Rechargeable 1.5V', user=self.user).save()

        # Return whatever was returned by the parent class
        return ret
