from django.db import models
from django.contrib.auth.models import User


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pictures")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="pictures")
    picture = models.ImageField(upload_to="game_pictures/")

    def __str__(self):
        return f"Picture {self.id} for {self.game.title} by {self.user.username}"
