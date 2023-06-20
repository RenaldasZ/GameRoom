from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        related_name="players",
        on_delete=models.CASCADE)
    score = models.PositiveIntegerField(_("Score"), db_index=True)
    played = models.DateTimeField(_("Played"), auto_now_add=True, null=True, blank=True)
    

    class Meta:
        ordering = ['played', 'score']
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("player_detail", kwargs={"pk": self.pk})

