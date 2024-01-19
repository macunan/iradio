from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Radios,Config
from .pyfunctions import Server_Ops
import os
from django.http import JsonResponse
from .forms import ConfigForm, RadioForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Import mimetypes module
import mimetypes
# import os module
# Import HttpResponse module
from django.http.response import HttpResponse



def index(request):
    transmit_status=False
    if request.method == "POST":
        if len(request.POST) == 1:
         ops=Server_Ops()
         ops.stop()
         Radios.objects.filter(state='ON').update(state='OFF')
         radios=Radios.objects.all().order_by('-state')
         frecuency = Config.objects.latest('id').frecuency
         context={'radios':radios,'frecuency':frecuency,'trans_status':transmit_status}
         return render(request,'radio.html',context)
        if len(request.POST) > 1:
            ops=Server_Ops()
            ops.writefile(request.POST["id"])
            Radios.objects.filter(state='ON').update(state='OFF')
            Radios.objects.filter(id=int(request.POST["id"])).update(state='ON')
            transmit_status=True
            ops.restart()
            radios=Radios.objects.all().order_by('-state')
            frecuency = Config.objects.latest('id').frecuency
            context={'radios':radios,'frecuency':frecuency,'trans_status':transmit_status}
            return render(request,'radio.html',context)



    radios=Radios.objects.all().order_by('statecount')
    frecuency = Config.objects.latest('id').frecuency
    context={'radios':radios,'frecuency':frecuency,'trans_status':transmit_status}
    return render(request,'radio.html',context)



# on_radio_id=Radios.objects.get(state="ON").id


def light(request):
    if request.method == "POST":
       D={'1':'/home/iradio/cron/mauri.sh',
            '2':'/home/iradio/cron/dad.sh',
            '3':'/home/iradio/cron/afuera.sh'}
       command=D[request.POST["id"]]
       os.system(command)
    return render(request,'light.html')

def cloud(request):
         ops=Server_Ops()
         files=ops.run_fast_scandir('/srv/http/books')
         print(files)
         context={'files':files}
         return render(request,'cloud.html',context)





def add(request):
    if request.method == 'POST':
        form=RadioForm(request.POST)
        if form.is_valid():
         form.save()
         context={'change':True ,'form':form}
         return render(request,'add.html',context)

    else:
       form=RadioForm()   
    context={'form':form}
    return render(request,'add.html',context)



def borrar(request):
        if request.method == "POST":
            radio=Radios.objects.get(id=int(request.POST["id"]))
            radio.delete()

        radios=Radios.objects.all().order_by('-id')
        context={'radios':radios}
        return render(request,'del.html',context)

def modify(request):
        if request.method == "POST":
            Radios.objects.filter(id=int(request.POST["id"])).update(name=request.POST["name"])
            Radios.objects.filter(id=int(request.POST["id"])).update(url=request.POST["url"])
            Radios.objects.filter(id=int(request.POST["id"])).update(bandwidth=request.POST["bandwidth"])
            radios=Radios.objects.all()
            context={'radios':radios,'change':True}
            return render(request,'modify.html',context)
        radios=Radios.objects.all().order_by('-state')
        context={'radios':radios}
        return render(request,'modify.html',context)







def ajax_view(request):
   if request.method == "POST":
        print(request.POST)
        radio=Radios.objects.get(id=int(request.POST["id"]))
        data = {
            "id": request.POST["id"],
            "name":radio.name,
            "url":radio.url,
            "bandwidth":radio.bandwidth
        }
        return JsonResponse(data)



def config(request):
    if request.method == 'POST':
        form=ConfigForm(request.POST)
        if form.is_valid():
         form.save()
         config = Config.objects.latest('id')
         filterid=config.id
         Config.objects.exclude(id=filterid).delete()
         server_op=Server_Ops()
         if  Radios.objects.filter(state="ON").count() > 0:
          on_radio_id=Radios.objects.get(state="ON").id
          server_op.writefile(on_radio_id)
          server_op.restart()
         context={'change':True ,'form':form}
         return render(request,'config.html',context)

    else:
       config = Config.objects.latest('id')
       form=ConfigForm(instance=config)   
    context={'form':form}
    return render(request,'config.html',context)



def download_file(request):
    config = Config.objects.latest('id')
    context={'change':True,'home':config.homelocation}
    # Define text file name
    filename = 'stations.csv'
    # Define the full file path
    filepath = config.homelocation+filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response



def export(request):
            
            ops=Server_Ops()
            config = Config.objects.latest('id')
            ops.export_stations()
            context={'change':True,'home':config.homelocation}
            return render(request,'export.html',context)

