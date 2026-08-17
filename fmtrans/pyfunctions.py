import os,glob
from subprocess import PIPE, run
from .models import Radios, Config

class Server_Ops:
    def stop(self):
       os.system("supervisorctl stop iradio")

    def restart(self):
       os.system("supervisorctl restart iradio")

    def writefile(self,id):
       id=int(id)
       config = Config.objects.latest('id')
       url=Radios.objects.get(id=id).url
       freq=config.frecuency
       home_loc=config.homelocation
       dma_channel=config.dma_channel
       bandwidth=Radios.objects.get(id=id).bandwidth
       radio_name=Radios.objects.get(id=id).name
       url_type=self.urltype(url)

       if len(radio_name)>64:
        radio_name=radio_name[0:64]

       if config.trans=="fm_transmitter":
        if url_type == "youtube":
         end=" -af 'highpass=f=30, lowpass=f=15000, compand=attacks=0.05:decays=0.2:points=-90/-90|-45/-14|-0/-4, volume=1.2'  -f wav -ac 2 -ar 22800 -  | fm_transmitter -f  "+freq+" -d 3 -b "+bandwidth+" -"
         init="#!/bin/bash"
         script="python3 /root/iradio/stream_audio.py "+url+" | ffmpeg -i - "+end
         file = open(home_loc+"radio.sh", "w")
         file.write(init+"\n")
         file.write(script)
         file.close()
         return

        if url_type == "ffmpeg":
         end=" -af 'highpass=f=30, lowpass=f=15000, compand=attacks=0.05:decays=0.2:points=-90/-90|-45/-14|-0/-4, volume=1.2'  -f wav -ac 2 -ar 22800 -  | fm_transmitter -f  "+freq+" -d 3 -b "+bandwidth+" -"
         init="#!/bin/sh"
         script="ffmpeg  -i "+url+end
         file = open(home_loc+"radio.sh", "w")
         file.write(init+"\n")
         file.write(script)
         file.close()
        else:
         end=" -r 22800 -c 2 -b 16 -t wav -  | fm_transmitter -f  "+freq+" -d 3 -b "+bandwidth+" -"
         init="#!/bin/sh"
         script="sox -t mp3 "+url+end
         file = open(home_loc+"radio.sh", "w")
         file.write(init+"\n")
         file.write(script)
         file.close()

       else:
        if url_type == "youtube":
         end=" -af 'highpass=f=30, lowpass=f=15000, compand=attacks=0.05:decays=0.2:points=-90/-90|-45/-14|-0/-4, volume=1.2'  -f wav -ac 2 -ar 22800 -  | pi_fm_rds -freq  "+freq+" -audio -"
         init="#!/bin/sh"
         script="python3 /root/iradio/stream_audio.py "+url+" | ffmpeg -i - "+end
         file = open(home_loc+"radio.sh", "w")
         file.write(init+"\n")
         file.write(script)
         file.close()
         return

        if url_type == "ffmpeg":
         end=" -af 'highpass=f=30, lowpass=f=15000, compand=attacks=0.05:decays=0.2:points=-90/-90|-45/-14|-0/-4, volume=1.2'  -f wav -ac 2 -ar 22800 - | pi_fm_rds -freq  "+freq+" -audio -"
         init="#!/bin/sh"
         script="ffmpeg  -i "+url+end
         file = open(home_loc+"radio.sh", "w")
         file.write(init+"\n")
         file.write(script)
         file.close()
        else:
         init="#!/bin/sh"
         end=" -r 22800 -c 2 -b 16 -t wav - | pi_fm_rds -freq  "+freq+" -audio -"
         script="sox -t mp3 "+url+end
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
            # files[i]=s.replace('/srv/nfs/books/','/static/')
            i=i+1
        return(files)

    def urltype(self,url):

        if "youtube" in url:
         url=url.replace("m.youtube","youtube")
         return "youtube"

        if "pls" in url:
         return "sox"

        if "m3u8" in url:
         return "ffmpeg"

        if "m3u" in url:
         return "sox"

        return "ffmpeg"


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

