from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from rest_framework import generics, permissions
from . import models, serializers
from django.views.generic import View
from django.db.models import Count, Avg, Sum
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


# Create your views here.
def index(request):
    return render(request, 'gameweb/index.html')


class HiScoreListView(View):
    def get(self, request):
        top_players = models.Player.objects.values('user__username').annotate(total_score=Sum('score'), score_count=Count('score')).order_by('-total_score')[:10]

        players_with_avg_ratio = []
        for player in top_players:
            username = player['user__username']
            total_score = player['total_score']
            score_count = player['score_count']
            avg_ratio = total_score / score_count if score_count != 0 else 0

            players_with_avg_ratio.append({'username': username, 'total_score': total_score, 'avg_ratio': f'{avg_ratio}'})

        context = {
            'top_players': players_with_avg_ratio
        }

        return render(request, 'gameweb/hiscore.html', context)


class PlayerList(generics.ListCreateAPIView):
    # queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Player.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MatchCreateList(generics.ListCreateAPIView):
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return models.Match.objects.filter(player2__isnull=True)

    def perform_create(self, serializer):
        serializer.save(player1=self.request.user)


class MatchDetailJoin(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return models.Match.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            match = models.Match.objects.get(pk=kwargs['pk'], player2__isnull=True)
        except Exception as e:
            raise ValidationError('You cannot join this game.')
        else:
            return self.update(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.player2 = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializers.MatchSerializer(instance).data)
