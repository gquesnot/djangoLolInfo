from django.urls import path

from historyInfo.views import Home, showMatch

urlpatterns = [
    path('', Home.as_view(), name="index"),
    path('match/<slug:matchId>', showMatch, name="matchById"),
]
