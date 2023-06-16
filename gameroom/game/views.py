from django.shortcuts import render
from django.views import generic
from .models import Player

# Create your views here.
def index(request):
    return render(request, 'gameweb/index.html')


class HiScoreListView(generic.ListView):
    model = Player
    template_name = "gameweb/hiscore.html"
