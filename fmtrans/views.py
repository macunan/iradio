from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Radios,Config
from .pyfunctions import Server_Ops
import os
from django.http import JsonResponse
from .forms import ConfigForm, RadioForm
def index(request):
    transmit_status=False
    if request.method == "POST":
        if len(request.POST) == 1:
         ops=Server_Ops()
         ops.stop()
         Radios.objects.filter(state='ON').update(state='OFF')
        if len(request.POST) > 1:
            ops=Server_Ops()
            ops.writefile(request.POST["id"])
            Radios.objects.filter(state='ON').update(state='OFF')
            Radios.objects.filter(id=int(request.POST["id"])).update(state='ON')
            transmit_status=True
            ops.restart()

# on_radio_id=Radios.objects.get(state="ON").id
    radios=Radios.objects.all().order_by('-state')
    frecuency = Config.objects.latest('id').frecuency
    context={'radios':radios,'frecuency':frecuency,'trans_status':transmit_status}
    return render(request,'radio.html',context)


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
            "url":radio.url
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
