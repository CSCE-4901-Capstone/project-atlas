from rest_framework import serializers
from api.models import FlightModel, AI_MessageHistory

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightModel
        fields = '__all__'

    def create(self, validated_data):
        icao24 = validated_data.get("icao24")

        # Check if a flight with the same icao24 already exists
        flight, created = FlightModel.objects.update_or_create(
            icao24=icao24, defaults=validated_data
        )

        print(f"Created: {created}, Flight: {flight}")  # Debugging print to check if update or create happens
        return flight


class AI_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AI_MessageHistory
        fields = '__all__'