from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="games_created"
    )
    title = models.CharField(max_length=255, unique=True)
    year_released = models.IntegerField()
    description = models.TextField()
    designer = models.CharField(max_length=255)
    number_of_players = models.IntegerField()
    estimated_playtime = models.IntegerField(help_text="Estimated playtime in minutes")
    recommended_age = models.IntegerField()
    categories = models.ManyToManyField(
        "Category", through="GameCategory", related_name="games"
    )
