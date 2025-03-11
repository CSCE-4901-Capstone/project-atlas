from django.db import models

class FlightModel(models.Model):
    # icao24 is the address of the plane
    icao24 = models.CharField(max_length=30, primary_key=True)
    callsign = models.CharField(max_length=8, null=True, blank=True)
    country = models.CharField(max_length=70)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    velocity = models.FloatField(null=True)
    direction = models.FloatField(null=True)
    category = models.IntegerField(null=True)

    def __str__(self):
        return self.callsign if self.callsign else self.icao24

    class Meta:
        ordering = ('icao24', )


