from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import CarSerializer, UploadFileSerializer
from .models import Car
from bs4 import BeautifulSoup

@extend_schema_view(
    upload_file=extend_schema(
        summary="Upload XML file and parse cars",
        request=UploadFileSerializer,
        responses={200: CarSerializer(many=True)}
    ),
    list_cars=extend_schema(
        summary="List all parsed cars",
        responses={200: CarSerializer(many=True)}
    ),
    clear_cars=extend_schema(
        summary="Clear parsed cars",
        responses={200: 'Successfully cleared cars', 500: 'Clearing failed'}
    ),
    retrieve_car=extend_schema(
        summary="Retrieve a car by index",
        responses={200: CarSerializer}
    )
)
class CarViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]
    cars = []

    def create(self, request):
        # POST /api/cars/upload_file/
        if request.method == 'POST':
            serializer = UploadFileSerializer(data=request.data)
            if serializer.is_valid():
                file = serializer.validated_data['file']
                soup = BeautifulSoup(file.read(), 'xml')
                cars = []
                for item in soup.find_all('car'):
                    car = Car(
                        make=item.find('make').text,
                        model=item.find('model').text,
                        year=int(item.find('year').text),
                        price=float(item.find('price').text)
                    )
                    cars.append(car)
                CarViewSet.cars = cars
                return Response(CarSerializer(cars, many=True).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        # GET /api/cars/
        if request.method == 'GET':
            return Response(CarSerializer(CarViewSet.cars, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request):
        # DELETE /api/cars/clear/
        if request.method == 'DELETE':
            CarViewSet.cars = []
            return Response("Successfully cleared cars", status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        # GET /api/cars/<int:pk>/
        if request.method == 'GET':
            try:
                car = CarViewSet.cars[int(pk)]
                return Response(CarSerializer(car).data, status=status.HTTP_200_OK)
            except (IndexError, ValueError):
                return Response("Car not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
