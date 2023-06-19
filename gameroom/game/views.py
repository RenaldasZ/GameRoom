from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from . models import Player
from django.views.generic import View


# Create your views here.
def index(request):
    return render(request, 'gameweb/index.html')


class HiScoreListView(View):
    def get(self, request):
        top_players = Player.objects.order_by('-score')[:10]

        context = {
            'top_players': top_players
        }

        return render(request, 'gameweb/hiscore.html', context)
