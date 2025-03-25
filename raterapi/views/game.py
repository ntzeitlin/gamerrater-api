from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game
from .users import UserSerializer
from .picture import PictureSerializer


class GameViewSet(ViewSet):
    """Game view set"""

    # ADD TRY EXCEPT STATEMENTS FOR EACH FOREIGN KEY REFERENCE / objects.get
    # LOOK AT EXAMPLE IN TIMECAPSULE CLASS PROJECT

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        game = Game()
        game.user = request.auth.user
        game.title = request.data["title"]
        game.year_released = request.data["year_released"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.number_of_players = request.data["number_of_players"]
        game.estimated_playtime = request.data["estimated_playtime"]
        game.recommended_age = request.data["recommended_age"]

        if (
            game.title is not None
            and game.year_released is not None
            and game.description is not None
            and game.designer is not None
            and game.number_of_players is not None
            and game.estimated_playtime is not None
            and game.recommended_age is not None
        ):

            game.save()
            category_ids = request.data.get("categories", [])
            game.categories.set(category_ids)

            try:
                serializer = GameSerializer(
                    game, many=False, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as ex:
                print("error:", ex)
                return Response(
                    {"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST
                )

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, many=False, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.user = request.auth.user
            game.title = request.data["title"]
            game.year_released = request.data["year_released"]
            game.description = request.data["description"]
            game.designer = request.data["designer"]
            game.number_of_players = request.data["number_of_players"]
            game.estimated_playtime = request.data["estimated_playtime"]
            game.recommended_age = request.data["recommended_age"]
            category_ids = request.data.get("categories", [])
            game.categories.set(category_ids)
            game.save()
        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
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
            search_text = self.request.query_params.get("q", None)
            sort_text = self.request.query_params.get("orderby", None)

            games = Game.objects.all()

            if search_text:
                games = Game.objects.filter(
                    Q(title__contains=search_text)
                    | Q(description__contains=search_text)
                    | Q(designer__contains=search_text)
                )

            if sort_text:
                games = Game.objects.order_by(sort_text)

            serializer = GameSerializer(games, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    # categories = CategorySerializer(many=True)
    pictures = PictureSerializer(many=True)
    user = UserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()

    # Since average_rating is declared as a @property and calculated in the game model,
    # add it here as a read only field.
    average_rating = serializers.ReadOnlyField()

    # Alternatively, could derive the value dynamically here in the serializer,
    #  using the .SerializerMethodField() method like is_owner.
    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    class Meta:
        model = Game
        fields = (
            "id",
            "user",
            "title",
            "year_released",
            "description",
            "designer",
            "number_of_players",
            "estimated_playtime",
            "recommended_age",
            "categories",
            "is_owner",
            "average_rating",
            "pictures",
        )
