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
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content.decode())

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "New Test Game")
        self.assertEqual(json_response["designer"], "NTZ")
        self.assertEqual(json_response["estimated_playtime"], 100)
        self.assertEqual(json_response["number_of_players"], 100)
