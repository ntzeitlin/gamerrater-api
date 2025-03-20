from django.db import models


class Review(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reviews")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.game.title} - {self.rating}"
