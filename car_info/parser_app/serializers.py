from rest_framework import serializers

class CarSerializer(serializers.Serializer):
    make = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    price = serializers.FloatField()

class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()

class UpdatePriceSerializer(serializers.Serializer):
    make = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    new_price = serializers.FloatField()
