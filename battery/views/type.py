from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from battery.forms import *

APPNAME = "battery/"

#
# battery types
#

@login_required
def type_index(request):
    types = BatteryType.objects.filter(user=request.user)
    return render(request, APPNAME + 'type_index.html', {'types': types})


@login_required
def type_detail(request, pk=None, create=True):
    # POST request = submission of a form which must be saved to DB
    if request.method == 'POST':
        form = BatteryTypeForm(request.POST)
        # Check if the form submitted by user (bound form) passes all the validation checks
        if form.is_valid():
            # Here no action needed on form so no need to extract the parameters from the 'cleaned_data' dict
            instance = form.save(commit=False)  # returns the BatteryType instance stored in form.instance
            instance.user = request.user  # Add user to BatteryModel
            if not create:  # Update an existing BatteryType
                instance.pk = pk  # primary key of the BatteryType to update

            instance.save()
            return redirect('battery:type')

        else:
            pass  # Form is not valid (i.e., it did not pass the validation checks)
            # is_valid() method created errors dict, so form reference now contains errors
            # this form reference drops to the last return statement where errors
            # can then be presented accessing form.errors in a template

    # GET request is either:
    # - for creating a new battery type => create=True
    # - view a battery type with pk=X => create=False
    else:
        if create:
            # generate blank form
            form = BatteryTypeForm()  # Reference is now an unbound (empty) form
        else:
            # Generate a form which is populated based on the QuerySet for type with primary-key = pk
            # Method 1
            # res = BatteryType.objects.filter(user=request.user).get(pk=pk)
            # form = BatteryTypeForm(initial=model_to_dict(res))  # populate the form based on the QuerySet
            # Method 2
            res = get_object_or_404(BatteryType, pk=pk, user=request.user)
            form = BatteryTypeForm(instance=res)

    # Hit if if method is GET
    # or if method is POST but form is not valid (ie, it fails form.is_valid())
    return render(request, APPNAME + 'type_detail.html', {'pk': pk, 'create': create, 'form': form})


@login_required
def type_delete(request, pk):
    # POST request = delete assignment
    if request.method == 'POST':
        type_ = get_object_or_404(BatteryType, pk=pk, user=request.user)
        type_.delete()
        return redirect('battery:type')
