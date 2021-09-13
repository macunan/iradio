import os,glob
from .models import Radios, Config

class Server_Ops:
    def stop(self):
       os.system("systemctl stop iradio")
    def restart(self):
       os.system("systemctl restart iradio")
    def writefile(self,id):
       id=int(id)

       config = Config.objects.latest('id')
       url=Radios.objects.get(id=id).url
       freq=config.frecuency
       home_loc=config.homelocation
       radio_name=Radios.objects.get(id=id).name
       if len(radio_name)>64:
        radio_name=radio_name[0:64]
       start="sox -t mp3 "
       end=" -t wav - |pi_fm_rds -freq "+freq+ "   -rt '"+radio_name+"' -audio -"
# end=" -r 22050 -c 1 -b 16 -t wav - |fm_transmitter -f  91.0 -"
       init="#!/bin/bash"
       script=start+url+end
       file = open(home_loc+"radio.sh", "w") 
       file.write(init+"\n")
       file.write(script)
       file.close()
    def run_fast_scandir(self,dir):    # dir: str, ext: list
        s="";
        i=0
        files = glob.glob(dir + '/**/*.*', recursive=True)
        while i<len(files):
            s=files[i]
# static/books/tarea1.png
# /srv/http/books/ebooksclub.org__NetBeans_IDE_7_Cookbook.pdf""
            files[i]=s.replace('/srv/http/','/static/')
            i=i+1 


        return(files)


    def export_stations(self):
       config = Config.objects.latest('id')
       home_loc=config.homelocation
       radios=Radios.objects.all()
       file = open(home_loc+"stations.csv", "w") 
       for radio in radios :
        print(radio.name)
        print(radio.url)
        file.write(radio.name+","+radio.url+"\n")
       file.close()

