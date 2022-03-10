from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelForm
from django.db.models import Sum

from battery import models
from battery.models import BatteryType, BatteryModel, BatteryAssignment, Device


#
# Form based on the model defined in models.py
#

class BatteryAssignmentForm(ModelForm):
    user = None     # need to store the user for the clean_battery_qty() validator

    class Meta:
        model = BatteryAssignment
        fields = ['device', 'battery_model', 'battery_qty']

    def __init__(self, user, *args, **kwargs):
        super(BatteryAssignmentForm, self).__init__(*args, **kwargs)
        # For the foreign keys: Only show the Devices and battery models associated for this user
        self.user = user
        self.fields['device'].queryset = models.Device.objects.filter(user=user)
        self.fields['battery_model'].queryset = models.BatteryModel.objects.filter(user=user)

    # Validator for battery_qty
    def clean_battery_qty(self):
        # The total nb of batteries assigned to a device must be no greater than the battery capacity of the device

        # Retrieve the battery capacity of the Device to which batteries are assigned
        dev = Device.objects.get(user=self.user, description=self.cleaned_data['device'].description)
        battery_capacity = dev.battery_qty  # Battery capacity for this Device

        # For all the battery assignments for this Device, the total of assigned batteries must be <= device capacity

        # The device name/description is not a property of the BatteryAssignment model.
        # It is a property of the Device model which is referenced in the BatteryAssignment model.
        # So I need to follow the 'device' key (SQL JOIN)
        # Since this is a QuerySet based on BatteryAssignment model I need to access the Device model fields
        # with the syntax: device__description
        assignments = BatteryAssignment.objects.select_related('device').filter(
            user=self.user, device__description=self.cleaned_data['device'].description)
        sum_ = assignments.aggregate(Sum('battery_qty'))  # return a dict like this: {'battery_qty__sum': 26}
        sum_ = sum_['battery_qty__sum'] if sum_['battery_qty__sum'] else 0

        # The sum_ contains the sum of all current assignments, including the one being updated
        # self.initial['battery_qty'] contains:
        # - 0 when a new assignment is created
        # - the nb of battery for the assignment before it is modified

        rest = battery_capacity - sum_ + self.initial['battery_qty']

        # Check the value
        if 1 <= self.cleaned_data['battery_qty'] <= rest:
            pass
        else:
            # raise an error
            battery_ies = "batteries" if rest > 1 else "battery"
            raise forms.ValidationError(f"No more than {rest} {battery_ies} can be assigned to this device.",
                                        code='incorrect_value')

        # Always return the value being validated
        return self.cleaned_data['battery_qty']


class BatteryAssignmentFormFilter(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(BatteryAssignmentFormFilter, self).__init__(*args, **kwargs)

        # Build dynamic choices from Model database entries
        # https://stackoverflow.com/questions/3419997/creating-a-dynamic-choice-field
        #
        # 'user' is added as an argument in __init__ constructor
        # then form objects are created in Views with either of:
        # - an unbound form is created with: form = AssignmentsViewForm(user=request.user)
        # - a bound form is created with:    form = AssignmentsViewForm(user=request.user, data=request.GET)
        #

        # battery_type
        # Build a choice of all battery types for the current user
        choices = [(o.id, str(o)) for o in BatteryType.objects.filter(user=user)]
        choices.insert(0, ('0', 'Select a battery type'))   # Add an instruction at the head of the list of choices
        self.fields['battery_type'] = forms.ChoiceField(label="", choices=choices, required=False)

        # battery_model
        # Build a choice of all battery models for the current user
        choices = [(o.id, str(o)) for o in BatteryModel.objects.filter(user=user)]
        choices.insert(0, ('0', 'Select a battery model'))  # Add an instruction at the head of the list of choices
        self.fields['battery_model'] = forms.ChoiceField(label="", choices=choices, required=False)


class BatteryModelForm(ModelForm):
    class Meta:
        model = BatteryModel
        fields = ['description']


class BatteryTypeForm(ModelForm):
    class Meta:
        model = BatteryType
        fields = ['type', 'description']


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['description', 'battery_type', 'battery_qty']

    def __init__(self, user, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        # For the foreign keys: Only show the battery types associated for this user
        self.fields['battery_type'].queryset = models.BatteryType.objects.filter(user=user)


class DeviceFormFilter(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(DeviceFormFilter, self).__init__(*args, **kwargs)

        # Build dynamic choices from Model database entries
        # https://stackoverflow.com/questions/3419997/creating-a-dynamic-choice-field
        #
        # 'user' is added as an argument in __init__ constructor
        # then form objects are created in Views with either of:
        # - an unbound form is created with: form = AssignmentsViewForm(user=request.user)
        # - a bound form is created with:    form = AssignmentsViewForm(user=request.user, data=request.GET)
        #

        # battery_type
        # Build a choice of all battery types for the current user
        choices = [(o.id, str(o)) for o in BatteryType.objects.filter(user=user)]
        choices.insert(0, ('0', 'Select a battery type'))  # Add an instruction at the head of the list of choices
        self.fields['battery_type'] = forms.ChoiceField(label="", choices=choices, required=False)
