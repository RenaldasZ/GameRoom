from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Match(models.Model):
    player1 = models.ForeignKey(User, verbose_name=_("Player 1"), related_name="created_matches", on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, verbose_name=_("Player 2"), related_name="joined_matches", on_delete=models.CASCADE, null=True, blank=True)
    played_at = models.DateTimeField(_("Played_at"), auto_now_add=True)

    class Meta:
        verbose_name = _("match")
        verbose_name_plural = _("matchs")

    def __str__(self):
        return f"{self.player1.get_username()}:{self.player2.get_username()}"

    def get_absolute_url(self):
        return reverse("match_detail", kwargs={"pk": self.pk})


# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        related_name="players",
        on_delete=models.CASCADE)
    score = models.PositiveIntegerField(_("Score"), db_index=True)
    played = models.DateTimeField(_("Played"), auto_now_add=True, null=True, blank=True)
    match = models.ForeignKey(Match, verbose_name=_("match"), on_delete=models.CASCADE, null=True, blank=True)
    

    class Meta:
        ordering = ['played', 'score']
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("player_detail", kwargs={"pk": self.pk})

