from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(BatteryType)
class BatteryTypeAdmin(admin.ModelAdmin):
    list_display = ("type", "description", "user")
    list_filter = ("user", )


@admin.register(BatteryModel)
class BatteryModelAdmin(admin.ModelAdmin):
    list_display = ("description", "user")
    list_filter = ("user", )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("description", "battery_type", "battery_qty", "user")
    list_filter = ("user", "battery_type",)


@admin.register(BatteryAssignment)
class BatteryAssignmentAdmin(admin.ModelAdmin):
    list_display = ("device", "battery_model", "battery_qty", "user")
    list_filter = ("user", "battery_model",)
