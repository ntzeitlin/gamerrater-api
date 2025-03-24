import uuid
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Picture, Game


class PictureViewSet(ViewSet):
    """Picture view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        picture = Picture()

        format, imgstr = request.data["game_image"].split(";base64,")
        ext = format.split("/")[-1]
        data = ContentFile(
            base64.b64decode(imgstr),
            name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}',
        )

        picture.picture = data

        try:
            picture.game = Game.objects.get(pk=request.data["game_id"])
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        picture.user = request.auth.user

        try:
            picture.save()
            serializer = PictureSerializer(picture)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            picture = Picture.objects.get(pk=pk)
            serializer = PictureSerializer(picture)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            pictures = Picture.objects.all()
            serializer = PictureSerializer(pictures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class PictureSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Picture
        fields = ("id", "user", "game", "picture")
