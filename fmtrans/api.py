
import os
from datetime import date
from typing import List
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from .models import Radios,Config
from typing import List
from .pyfunctions import Server_Ops
api = NinjaAPI()


class Config_in(Schema):
    frecuency: str
    id: int
    homelocation: str 

class Radios_out(Schema):
    id: int
    name: str
    url: str
    state:str


class Radios_in(Schema):
    name: str
    url: str

class Toggle_in(Schema):
    id: int

@api.post("/create_radio")
def create_radio(request, payload: Radios_in):
    radio = Radios.objects.create(**payload.dict())
    return {"id": radio.id}


@api.get("/radio_list", response=List[Radios_out])
def list_radios(request):
    qs = Radios.objects.all()
    return qs

@api.put("/update_radio/{id}")
def update_radio(request, id: int, payload: Radios_in):
    radio = get_object_or_404(Radios, id=id)
    for attr, value in payload.dict().items():
        setattr(radio, attr, value)
    radio.save()
    return {"success": True}



@api.put("/toggle_radio/{id}")
def toggle_radio(request, id: int, payload: Toggle_in):
    radio = get_object_or_404(Radios, id=id)
    if radio.state == 'ON':
       radio.state='OFF'
       ops=Server_Ops()
       ops.stop()
       radio.save()
       return {"transmit_status": False}
    else:
       ops=Server_Ops()
       ops.writefile(id)
       Radios.objects.filter(state='ON').update(state='OFF')
       ops.restart()
       radio.state='ON'
       radio.save()
       return {"transmit_status": True}


@api.delete("/delete_radio/{id}")
def delete_radio(request, id: int):
    radio= get_object_or_404(Radios, id=id)
    radio.delete()
    return {"success": True}


@api.get("/radio_get/{id}", response=Radios_out)
def get_radio(request, id: int):
    radio = get_object_or_404(Radios, id=id)
    return radio


@api.get("/get_config", response=List[Config_in])
def get_config(request):
    qs  = Config.objects.latest('id')
    return qs


@api.get("/export") 
def export_radio(request):
            ops=Server_Ops()
            config = Config.objects.latest('id')
            ops.export_stations()
            return {"success": config.homelocation,'change':True}


