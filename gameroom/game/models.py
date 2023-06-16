from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Player(models.Model):
    name = models.ForeignKey(
        User,
        verbose_name=_("name"),
        related_name="players",
        on_delete=models.CASCADE)
    score = models.PositiveIntegerField(_("Score"))
    

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("player_detail", kwargs={"pk": self.pk})

