from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from battery.forms import *

APPNAME = "battery/"

#
# battery assignments
#

@login_required
def assignment(request):
    # Only a GET request is valid
    # But there is no need to check the method used for this request since the template is protected with CSRF
    # and if a non-GET is received, django replies with "403 Forbidden" because of lack of valid CSRF in request

    # if the GET request contains a parameter then a bound form must be created
    if request.GET.get('battery_type'):
        form = BatteryAssignmentFormFilter(user=request.user, data=request.GET)
        # Check if the bound form submitted by user passes all the validation checks
        if form.is_valid():
            # extract the parameters from the cleaned_data dict
            battery_type_filter = form.cleaned_data['battery_type']
            battery_model_filter = form.cleaned_data['battery_model']

            # Generate the filter as a dict which is subsequently passed expanded (with '**') to the .filter() method

            if battery_type_filter == '0' and battery_model_filter == '0':  # filter only on user
                assignment_filter = {"user": request.user}
            elif battery_type_filter == '0':  # filter on user & battery_model
                assignment_filter = {"user": request.user, "battery_model": battery_model_filter}
            elif battery_model_filter == '0':  # filter on user & battery_type
                assignment_filter = {"user": request.user, "device__battery_type": battery_type_filter}
            else:  # filter on user, battery_model and battery_type (need to follow the 'device' key)
                assignment_filter = {"user": request.user, "battery_model": battery_model_filter,
                                     "device__battery_type": battery_type_filter}

            # battery_type is not a property of the BatteryAssignment model.
            # It is a property of the Device model which is referenced in the BatteryAssignment model.
            # So I need to follow the 'device' key (SQL JOIN)
            # Since this is a QuerySet based on BatteryAssignment model I need to access the Device model fields
            # with the syntax: device__battery_type
            assignments = BatteryAssignment.objects.select_related('device').filter(**assignment_filter)

        else:
            pass  # Form is not valid (i.e., it did not pass the validation checks)
            # is_valid() method created errors dict, so 'form' now contains errors
            # this form reference drops to the last return statement where errors
            # can then be presented accessing form.errors in a template

    # GET request without filter parameters = show all battery assignments for this user
    else:
        form = BatteryAssignmentFormFilter(user=request.user)
        assignments = BatteryAssignment.objects.filter(user=request.user)

    # Calculate total nb of battery used for the assignments and render the page
    qsum = assignments.aggregate(Sum('battery_qty'))  # return a dict like this: {'battery_qty__sum': 26}
    return render(request, APPNAME + 'assignment_index.html',
                  {'form': form, 'assignments': assignments, 'battery_total': qsum['battery_qty__sum']})


'''
detail of a battery assignment
    pk = primary key of an assignment being viewed/updated
    create = boolean 'True' when creating a new assignment, 'False' when viewing/updating an existing assignment
'''


@login_required
def assignment_detail(request, pk=None, create=True):
    # POST request = submission of a form which must be saved to DB
    if request.method == 'POST':
        form = BatteryAssignmentForm(data=request.POST, user=request.user)

        # For form validation, need to know the battery_qty of the assignment in the DB which will be updated
        if create:  # Create an assignment, use an initial battery_qty of 0 for validation
            form.initial['battery_qty'] = 0  # Add this info to the form for validation
        else:  # Update an assignment, retrieve the initial battery_qty of the assignment being updated
            # Need to check the battery_qty of the assignment being updated
            instance = get_object_or_404(BatteryAssignment, pk=pk, user=request.user)  # retrieve the BA being updated
            form.initial['battery_qty'] = instance.battery_qty  # Add this info to the form for validation

        # Check if the form submitted by user (bound form) passes all the validation checks
        if form.is_valid():
            # Here no action needed on the form, no need to extract the parameters from the 'cleaned_data' dict
            instance = form.save(commit=False)  # returns the BatteryAssignment instance stored in form.instance
            instance.user = request.user  # Add user to the BatteryAssignment

            if not create:  # Update an BatteryAssignment
                instance.pk = pk  # primary key of the BatteryAssignment to update

            instance.save()  # save the BatteryAssignment to the DB
            return redirect('battery:assignment')

        else:
            pass  # Form is not valid (i.e., it did not pass the validation checks)
            # is_valid() method created errors dict, so form reference now contains errors
            # this form reference drops to the last return statement where errors
            # can then be presented accessing form.errors in a template

    # GET request is either:
    # - for creating a new assignment => create=True
    # - view assignment with pk=X => create=False
    else:
        if create:
            # generate blank form
            form = BatteryAssignmentForm(user=request.user,
                                         initial={'battery_qty': 1})  # Reference is now an unbound (empty) form
        else:
            # Generate a form which is populated based on the QuerySet for assignment with primary-key = pk
            # Method 1
            # assign = BatteryAssignment.objects.filter(user=request.user).get(pk=pk)
            # form = BatteryAssignmentForm(initial=model_to_dict(assign))  # populate the form based on the QuerySet
            # Method 2
            instance = get_object_or_404(BatteryAssignment, pk=pk, user=request.user)  # return a BA instance
            form = BatteryAssignmentForm(user=request.user, instance=instance)  # create form with User and BA instances

    # Hit if if method is GET
    # or if method is POST but form is not valid (ie, it fails form.is_valid())
    return render(request, APPNAME + 'assignment_detail.html', {'pk': pk, 'create': create, 'form': form})


@login_required
def assignment_delete(request, pk):
    # POST request = delete assignment
    if request.method == 'POST':
        assign = get_object_or_404(BatteryAssignment, pk=pk, user=request.user)  # returns BA instance
        assign.delete()
        return redirect('battery:assignment')
    else:
        # GET request = render confirmation page for deletion
        # This is Historic, there is now a Bootstrap Modal in the page which allows to confirm deletion locally
        # So, only a POST for deletion should now be received
        return render(request, APPNAME + '__old__assignment_delete.html', {'pk': pk})
