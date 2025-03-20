from django.db import models


class GamePicture(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    picture = models.ForeignKey("Picture", on_delete=models.CASCADE)
