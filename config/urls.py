from django.conf import settings
from django.contrib import admin
from django.urls import path, include

import battery.views

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),

    # override the SignupView of django-allauth
    path("accounts/signup/", view=battery.views.AccountSignupView.as_view()),
    # this is the default config for django-allauth
    path('accounts/', include('allauth.urls')),

    path('battery/', include('battery.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
