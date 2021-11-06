from django.shortcuts import render

# Create your views here.
from django.views import View


def showMatch(request, matchId):
    return render(request, 'match.html', {
        "matchId": matchId
    })

class Home(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        self.get(request)