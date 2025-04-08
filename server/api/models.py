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


class AI_MessageHistory(models.Model):          #model defined for API communication with Google Gemini
    session_id = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): #definition of string representation of AI response
        return f"[{self.timestamp}] {self.role}: {self.content[:30]}"