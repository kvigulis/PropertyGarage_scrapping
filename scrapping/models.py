from django.db import models
import datetime


class ResultProperty(models.Model):
    date = models.DateTimeField(db_column='result:date', default=False)
    title = models.CharField(max_length=60, default="Title ERROR")
    price = models.CharField(max_length=20, default="Price ERROR")
    property_id = models.IntegerField(db_column='result:id', null=True, blank=True, default=0)
    URL = models.CharField(max_length=200, default="")
    favourite = models.BooleanField(default=False)
    best = models.BooleanField(default=False)

    def __str__(self):
        return "Property - price {}; ID: {} - {}".format(
            self.price,
            self.property_id,
            self.date
        )

