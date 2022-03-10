from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import CustomUser


# Create your models here.

# This class will be mapped to a database schema with "./manage.py makemigrations"
# the DB will be migrated with "./manage.py migrate"

class BatteryType(models.Model):
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # string representation
    def __str__(self):
        # return "%s (%s)" % (self.type, self.description)
        return self.type


class Device(models.Model):
    description = models.CharField(max_length=100)
    battery_type = models.ForeignKey(BatteryType, on_delete=models.CASCADE)
    battery_qty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # string representation
    def __str__(self):
        return "%s (%sx %s)" % (self.description, self.battery_qty, self.battery_type)


class BatteryModel(models.Model):
    description = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # string representation
    def __str__(self):
        return self.description


class BatteryAssignment(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    battery_model = models.ForeignKey(BatteryModel, on_delete=models.CASCADE)
    # todo: limit the MaxValue to the battery_qty of the associated Device
    # battery_qty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    battery_qty = models.PositiveSmallIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # string representation
    def __str__(self):
        return "%s (%sx %s)" % (self.device, self.battery_qty, self.battery_model)
