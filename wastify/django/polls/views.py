from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    # This is how you get variables from the url
    print(request.GET['username']) # => [39]
    print(request.GET['password']) # => [39]
    #this works
    return HttpResponse(request.GET['password'])

    # for url: http://localhost:4000/polls/?username=alex&password=pw1