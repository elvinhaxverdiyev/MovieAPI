from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from movieapp.models.actors_models import Actor
from movieapp.serializers.actors_serializers import ActorsSerializer

__all__ = [
    "ActorsAPIView"
]

class ActorsAPIView(APIView):
    http_method_names = ['get']
    @swagger_auto_schema(
        operation_description="Bütün aktyorların siyahısını gətirir",
        responses={200: ActorsSerializer(many=True)}
    )
    def get(self, request):
        actor = Actor.objects.all()
        serializer = ActorsSerializer(actor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)