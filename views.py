from django.http import HttpResponse

def index(request):
    return HttpResponse("Listado de radios")
