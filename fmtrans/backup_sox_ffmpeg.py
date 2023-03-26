import os,glob
from subprocess import PIPE, run
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
       wav_location=config.wavlocation
       dma_channel=config.dma_channel
       bandwidth=config.bandwidth
       radio_name=Radios.objects.get(id=id).name
       url_type=self.urltype(url)
       if len(radio_name)>64:
        radio_name=radio_name[0:64]
       if url_type == "ffmpeg":
        end=" -f wav -bitexact -acodec pcm_s16le -ar 44100 -ac 2 -y" +" "+wav_location+"radio.wav &" 
        end2=" sleep 5"+ "\n"+" fm_transmitter -f "+freq+" -d 3 -b "+bandwidth+ " "+wav_location+"radio.wav"
# end2=" sleep 5"+ "\n"+" fm_transmitter -f "+freq+" -d 3  "+wav_location+"radio.wav"

# start="curl "+url+"|egrep -o 'https?:.*'|tail -n 1"
# os.system(start+" > "+home_loc+"radio.sh")
# f = open(home_loc+"radio.sh", "r")
# initial=f.read()
# f.close()
# initial=initial.rstrip()
# end=" -t wav - |pi_fm_adv --freq "+freq+ " --rt '"+radio_name+"' --audio -"
# end="  -r 44100 -b 16 -e signed -t wav - |fm_transmitter -f  91.5 -"
# end=" -r 22050 -c 1 -b 16 -t wav - |fm_transmitter -f "+freq+" -d 3 -"
# end=" -r 22050 -b 16 -e signed -t wav - |fm_transmitter -f "+freq+" -d 3 -"
# end=" -r 44100 -b 16 -e signed -t wav - |fm_transmitter -f "+freq+" -d 3 -"
# end=" -ar 44100  -f wav - |fm_transmitter -f "+freq+" -d 3 -"

        init="#!/bin/bash"
# script=start+url+end
        script="nohup ffmpeg -i "+url+end
        file = open(home_loc+"radio.sh", "w")
        file.write(init+"\n")
        file.write(script)
        file.write(end2)
        file.close()
       else:
        start="sox -t mp3  "

# start="ffmpeg -i "
# end=" -t wav - |pi_fm_adv --freq "+freq+ " --rt '"+radio_name+"' --audio -"
# end="  -r 44100 -b 16 -e signed -t wav - |fm_transmitter -f  91.5 -"
# end=" -r 22050 -c 1 -b 16 -t wav - |fm_transmitter -f "+freq+" -d 3 -"
# end=" -r 22050 -b 16 -e signed -t wav - |fm_transmitter -f "+freq+" -d 3 -"
        end=" -r 44100 -b 16 -e signed -t wav - |fm_transmitter -f "+freq+" -d "+dma_channel+ " -b "+bandwidth+" -"
# end=" -ar 44100  -f wav - |fm_transmitter -f "+freq+" -d 3 -"

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
    def urltype(self,url):
        if "pls" in url:
         return "sox"
        if "m3u" in url:
         return "sox"
        if "mp3" in url:
         return "sox"
        if "aac" in url:
         return "ffmpeg"
        return "sox"


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

