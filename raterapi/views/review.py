from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Review, Game
from .game import GameSerializer
from .users import UserSerializer


class ReviewViewSet(ViewSet):
    """Review view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        review = Review()
        review.user = request.auth.user

        game = request.data.get("game")
        if not game:
            return Response(
                {"error": "Game ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game_instance = Game.objects.get(pk=game)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND
            )

        review.game = game_instance
        review.comment = request.data.get("comment", "")
        review.rating = request.data.get("rating", 0)
        review.save()

        try:
            serializer = ReviewSerializer(
                review, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(
                review, many=False, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk=None):
    #     """Handle PUT requests

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     try:
    #         review = Review.objects.get(pk=pk)
    #         review.sample_name = request.data["name"]
    #         review.sample_description = request.data["description"]
    #         review.save()
    #     except Review.DoesNotExist:
    #         return Response(None, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            reviews = Review.objects.all()
            serializer = ReviewSerializer(
                reviews, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    game = GameSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Review
        fields = ("id", "user", "game", "comment", "rating")
