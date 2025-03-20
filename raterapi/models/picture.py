from django.db import models


class Picture(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="pictures")
    game = models.ManyToManyField(
        "Game", through="GamePicture", related_name="pictures"
    )
    picture = models.ImageField(upload_to="game_pictures/")

    def __str__(self):
        return f"Picture {self.id} by {self.user.username}"
