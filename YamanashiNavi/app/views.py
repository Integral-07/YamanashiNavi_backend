from django.shortcuts import render

def index(request):

    params = {

        'title' : 'Hello Index!!',
    }

    return render(request, 'app/index.html', params)
