import os,glob
from .models import Radios, Config

class Server_Ops:
    def stop(self):
       os.system("systemctl stop iradio")
    def restart(self):
       os.system("systemctl restart iradio")
    def writefile(self,id):
       id=int(id)
       url=Radios.objects.get(id=id).url
       start="sox -t mp3 "
       end=" -t wav - |pi_fm_rds -freq  91.5.0 -audio -"
# end=" -r 22050 -c 1 -b 16 -t wav - |fm_transmitter -f  91.0 -"
       init="#!/bin/bash"
       script=start+url+end
       file = open(r"/home/iradio/radio.sh", "w") 
       file.write(init+"\n")
       file.write(script)
       file.close()
       print(script)
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

