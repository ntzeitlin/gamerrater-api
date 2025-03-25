import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapi.models import Game


class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ["users", "tokens", "games", "categories", "reviews"]

    def setUp(self):
        self.game = Game.objects.first()
        token = Token.objects.get(user=self.game.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/games"

        # Define the request body
        data = {
            "title": "New Test Game",
            "categories": [1],
            "year_released": 1988,
            "description": "Test Game for Test Suite",
            "designer": "NTZ",
            "number_of_players": 100,
            "estimated_playtime": 100,
            "recommended_age": 9,
        }

        # Initiate request and store response
        response = self.client.post(url, data, format="json")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "New Test Game")
        self.assertEqual(json_response["designer"], "NTZ")
        self.assertEqual(json_response["estimated_playtime"], 100)
        self.assertEqual(json_response["number_of_players"], 100)

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.id = 1
        game.title = "Test Game"
        game.year_released = 1987
        game.description = "That suckssss"
        game.designer = "New Designer"
        game.number_of_players = 20
        game.estimated_playtime = 1010
        game.recommended_age = 30
        game.user_id = 1
        game.categories.set([2])
        game.save()

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Test Game")
        self.assertEqual(json_response["year_released"], 1987)
        self.assertEqual(json_response["categories"], [2])
        self.assertEqual(json_response["description"], "That suckssss")
        self.assertEqual(json_response["designer"], "New Designer")
