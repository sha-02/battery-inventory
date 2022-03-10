from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from battery.forms import *

APPNAME = "battery/"

#
# Devices
#

@login_required
def device(request):
    # Only a GET request is valid
    # But there is no need to check the method used for this request since the template is protected with CSRF
    # and if a non-GET is received, django replies with "403 Forbidden" because of lack of valid CSRF in request

    # if the GET request contains a parameter then a bound form must be created
    if request.GET.get('battery_type'):
        form = DeviceFormFilter(user=request.user, data=request.GET)
        # Check if the bound form submitted by user passes all the validation checks
        if form.is_valid():
            # extract the parameters from the cleaned_data dict
            if form.cleaned_data['battery_type'] == '0':  # filter only on user
                devices = Device.objects.filter(user=request.user)
            else:  # filter on user and battery_type
                devices = Device.objects.filter(user=request.user, battery_type=form.cleaned_data['battery_type'])
        else:
            pass  # Form is not valid (i.e., it did not pass the validation checks)
            # is_valid() method created errors dict, so 'form' now contains errors
            # this form reference drops to the last return statement where errors
            # can then be presented accessing form.errors in a template

    # GET request without filter parameters = show all devices of the user
    else:
        form = DeviceFormFilter(user=request.user)
        devices = Device.objects.filter(user=request.user)

    # Calculate total nb of battery used by all devices and render the page
    qsum = devices.aggregate(Sum('battery_qty'))  # return a dict like this: {'battery_qty__sum': 26}
    return render(request, APPNAME + 'device_index.html',
                  {'form': form, 'devices': devices, 'battery_total': qsum['battery_qty__sum']})


@login_required
def device_detail(request, pk=None, create=True):
    # POST request = submission of a form which must be saved to DB
    if request.method == 'POST':
        form = DeviceForm(data=request.POST, user=request.user)
        # Check if the form submitted by user (bound form) passes all the validation checks
        if form.is_valid():
            # Here no action needed on the form, no need to extract the parameters from the 'cleaned_data' dict
            instance = form.save(commit=False)  # returns the Device instance stored in form.instance
            instance.user = request.user  # Add user to Device

            if not create:  # Update an existing battery device
                instance.pk = pk  # primary key of the Device to update

            instance.save()  # save the Device to the DB

            return redirect('battery:device')

        else:
            pass  # Form is not valid (i.e., it did not pass the validation checks)
            # is_valid() method created errors dict, so form reference now contains errors
            # this form reference drops to the last return statement where errors
            # can then be presented accessing form.errors in a template

    # GET request is either:
    # - for creating a new battery device => create=True
    # - view a battery device with pk=X => create=False
    else:
        if create:
            # generate blank form
            form = DeviceForm(user=request.user, initial={'battery_qty': 1})  # Reference is now an unbound (empty) form
        else:
            # Generate a form which is populated based on the QuerySet for device with primary-key = pk
            # Method 1
            # res = Device.objects.filter(user=request.user).get(pk=pk)
            # form = DeviceForm(initial=model_to_dict(res))  # populate the form based on the QuerySet
            # Method 2
            instance = get_object_or_404(Device, pk=pk, user=request.user)  # returns Device instance
            form = DeviceForm(user=request.user, instance=instance)  # add Device instance to a form

    # Hit if if method is GET
    # or if method is POST but form is not valid (ie, it fails form.is_valid())
    return render(request, APPNAME + 'device_detail.html', {'pk': pk, 'create': create, 'form': form})


@login_required
def device_delete(request, pk):
    # POST request = delete assignment
    if request.method == 'POST':
        dev = get_object_or_404(Device, pk=pk, user=request.user)
        dev.delete()
        return redirect('battery:device')
