from django.urls import path

from battery import views

# The 'name' of the paths are used in templates (html) and must be unique across whole apps of the project
# By registering a name for this app with variable 'app_name' it creates a context
# In the templates, the name must be referenced with {% url '<app_name>:<path.name>' %}
app_name = 'battery'

urlpatterns = [
    #
    # Assignments
    #
    # CRUD for battery assignments
    path('assignment', views.assignment, name='assignment'),
    # Use same view for creating and updating an assignment
    # Pass an extra argument ('create') to distinguish between create and update (which uses 'pk' as primary key)
    path('assignment/create', views.assignment_detail, name='assignment_create'),
    path('assignment/<int:pk>', views.assignment_detail, {'create': False}, name='assignment_detail'),
    path('assignment/<int:pk>/delete', views.assignment_delete, name='assignment_delete'),
    #
    # CRUD for battery models
    path('model', views.model, name='model'),
    path('model/create', views.model_detail, name='model_create'),
    path('model/<int:pk>', views.model_detail, {'create': False}, name='model_detail'),
    path('model/<int:pk>/delete', views.model_delete, name='model_delete'),
    #
    # CRUD for battery types
    path('type', views.type_index, name='type'),
    path('type/create', views.type_detail, name='type_create'),
    path('type/<int:pk>', views.type_detail, {'create': False}, name='type_detail'),
    path('type/<int:pk>/delete', views.type_delete, name='type_delete'),
    #
    # CRUD for devices
    path('device', views.device, name='device'),
    path('device/create', views.device_detail, name='device_create'),
    path('device/<int:pk>', views.device_detail, {'create': False}, name='device_detail'),
    path('device/<int:pk>/delete', views.device_delete, name='device_delete'),

    # For test debug
    # path('test', views.test, name='test'),
]
