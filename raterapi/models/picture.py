from django.db import models
from django.contrib.auth.models import User


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pictures")
    game = models.ForeignKey(
        "Game", on_delete=models.DO_NOTHING, related_name="pictures"
    )
    picture = models.ImageField(
        upload_to="actionimages",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )
