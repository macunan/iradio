# _Raspberry Pi FM Radio Transmitter_

![Alt Text](https://github.com/macunan/iradio/blob/main/iradio.gif)


- Iradio is browser based controller to transmitt FM radio from your Rasberry pi uses Django as front end and python together with the awesome RM Radio transmitter  by Christophe Jaquet and Arch Linux Arm Branch 

- https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3
 
- https://github.com/markondej/fm_transmitter
-https://github.com/FFmpeg

- Note You can transmit local mp3/aac files or remote url streams of your favorite internet radios stations.

- Latest change added variable bandwidth for each station

# Requirements
- Linux Instalation running on Raspbery pi 3b+ board.
- Small connector cable for GPIO 4 (pin 7 on header P1).
- A bit of time and effort.
- Good power supply for your raspberry pi.
- Fm Receiver so you can listen to your internet radio  or mp3/aac.
- Computer or phone/tablet to follow all steps.
- ssh access your raspberry pi and root like user to execute backend commands
- Install sox pacman -S sox and download and compile ffmmpeg to support https streams
- Be careful with your country/state regulations regarding FM  transmissions is your responsibility to follow them and comply with local laws and regulations in your region.
# Installation

1-  I used Arch linux arm for my installation but I believe it can be any Linux as long as you have a recent kernel in my case 5.10.60-1-ARCH #1 SMP Sat Aug 21 14:56:38 UTC 2021 armv7l GNU/Linux it should be fine. Note only recent Kernel will function without issues, older kernel might work but you might face some issues.

2- 
```sh
Clone the source repository and run make in the src directory:

git clone https://github.com/markondej/fm_transmitter
cd fm_transmitter
make

```

Make sure you have all the required libraries and compilers installed  like gcc and python installed

If make reports no error (i.e. the fm_transmitter executable gets generated), you can then simply run:
```sh
sudo ./fm_transmitter
```
This will generate an FM transmission on 107.9 MHz, with default station name (PS), radiotext (RT) and PI-code, without audio. The radiofrequency signal is emitted on GPIO 4 (pin 7 on header P1).


Once compiled copy to your systems's bin directory in my case for Arch Linux:
```sh
/usr/local/bin
[root@mauripi bin]# ls -lhtr 
cp pi_fm_rds /usr/local/bin
-rwxr-xr-x 1 root root  82K ago 26 18:56 fm_transmitter


```

From there you should be to execute from any directory, note this should be executed by root like user.

I created a iradio user:
```sh
cat /etc/passwd
iradio:x:0:0:root:/home/iradio:/bin/bash
```

Once you are sure the latter is installed and transmitting correctly proceed with next step:

3a-
Install sox in my OS command is pacman -S sox, also in ubuntu like systems it can be sudo apt-get install sox

Make sure sox is able to play local and remote streams
Example
```sh
sox  https://api.spreaker.com/listen/user/kgra/episode/latest/shoutcast.mp3
```
If you get any errors try a url that you know that works and try again if not you might need to compile sox from source.

3b-
Added ffmpeg functionality to play aac streams also you can play mp3 and aac files and transmit. But ffmpeg does not support playlist like pls and m3u formats, for that the program  checks your radio url and if it detects playlist file it goes back to sox above. However you need to compile ffmpeg to support aac and https with --enable-openssl option

```sh
git clone https://github.com/FFmpeg
cd ffmpeg

```
Ideally the following config  might need to install some codecs and libraries


```sh
./configure   --enable-nonfree --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libopus --enable-libvorbis --enable-libvpx --enable-libx264 --enable-libx265 --enable-openssl --enable-gpl --enable-omx --enable-omx-rpi --enable-mmal


make -j2
make install

```
if above does not work google is your friend and try to use less options in the configure part:

```sh
./configure   --enable-nonfree --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libopus --enable-libvorbis --enable-libvpx --enable-openssl --enable-gpl
make -j2
make install
```


If everything ok you should get something like this

```sh
 ffmpeg -
ffmpeg version git-2023-02-16-aeceefa6 Copyright (c) 2000-2023 the FFmpeg developers
  built with gcc 12.1.0 (GCC)
  configuration: --enable-nonfree --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libopus --enable-libvorbis --enable-libvpx --enable-libx264 --enable-libx265 --enable-openssl --enable-gpl --enable-omx --enable-omx-rpi --enable-mmal
  libavutil      58.  1.100 / 58.  1.100
  libavcodec     60.  2.100 / 60.  2.100
  libavformat    60.  2.100 / 60.  2.100
  libavdevice    60.  0.100 / 60.  0.100
  libavfilter     9.  2.100 /  9.  2.100
  libswscale      7.  0.100 /  7.  0.100
  libswresample   4.  9.100 /  4.  9.100
  libpostproc    57.  0.100 / 57.  0.100

```

Compiling ffmpeg was the harders part for me, I recommend complete update before starting
pacman -Syu then try again and try installing missing packages

But once finished very low cpu usage so well worth it:
```sh
Tasks: 178 total,   1 running, 177 sleeping,   0 stopped,   0 zombie
%Cpu(s):  7,8 us,  2,1 sy,  0,0 ni, 89,1 id,  0,9 wa,  0,0 hi,  0,1 si,  0,0 st
MiB Mem :    869,1 total,    263,4 free,    230,8 used,    374,8 buff/cache
MiB Swap:      0,0 total,      0,0 free,      0,0 used.    622,0 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND                                             
15193 root      20   0       0      0      0 I   7,6   0,0   0:09.27 kworker/2:0-events_freezable                        
14089 root      20   0   25116   3636   3112 S   3,0   0,4   0:39.34 fm_transmitter                                      
14088 root      20   0  108964  21204  17568 S   2,3   2,4   0:33.80 ffmpeg                                              
12451 root      20   0       0      0      0 I   1,3   0,0   1:11.86 kworker/2:1-events                                  
15713 root      20   0   11800   3280   2764 R   1,3   0,4   0:00.29 top                                                 
    1 root      20   0   37136   9092   6864 S   1,0   1,0  28:45.24 systemd                                             
  369 root      20   0   15140   5892   5200 S   0,7   0,7   2:26.54 systemd-logind                                      
  171 root      20   0       0      0     

```

4- Install Python and Django and tmux

-Install Python and Python installer
```sh
pacman -S python python-pip tmux
```
-Install Django
```sh
pip install django


```
Install django-ninja for backend api can be used with frontend frameworks instead of django templates.

```sh
pip install django-ninja

```


5- Install and configure Django source code
-In a directory that you have webserver access:
```sh
git clone  https://github.com/macunan/iradio
```

6- Install and configure systemd iradio.service
- As root like user navigate to:
```sh
cd /etc/systemd/system
the create file

nano iradio.service

and add the following:

[Unit]
Description=fmtranservice
[Service]
KillMode=none
ExecStart=/home/iradio/radio.sh
ExecStop=/home/iradio/stopiradio.sh
PIDFile=/var/run/fmtrans.pid
Restart=always
RestartSec=30
[Install]
WantedBy=multi-user.target

```
Close and save
```sh
systemctl enable iradio.service
```
Note the service will use /home/iradio/radio.sh to start and  to stop the radio

[root@mauripi ~]# cat stopiradio.sh 
#!/bin/bash
ps -ef | grep -v grep | grep fm_transmitter | awk '{print $2}'|xargs kill -INT


, the file
looks like the following:
```sh
#!/bin/bash
sox -t mp3 https://api.spreaker.com/listen/user/kgra/episode/latest/shoutcast.mp3 -t wav - |fm_transmitter -f  91.5 -
 ```

Note you can configure location in config section in the menu and also the transmitting frecuency.
Note homelocation referes of where radio.sh will be located. Systemd is used to start and stop the radio transmission.




7- execute tmux and run
In ssh session open new tmux session by typing tmux screen should be green and go to directory
where you cloned the iradio and find manage.py and execute the following:


```sh
 ./manage.py runserver 0.0.0.0:80
 ```
 You should get the following:
```sh
[root@mauripi raspberrypi_fmradio]# ./manage.py runserver 0.0.0.0:80
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 1 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): fmtrans.
Run 'python manage.py migrate' to apply them.
September 02, 2021 - 23:52:52
Django version 3.2.7, using settings 'raspberrypi_fmradio.settings'
Starting development server at http://0.0.0.0:80/
Quit the server with CONTROL-C.
```
Note the latter will last until the raspberry pi is powered down or rebooted, so you will need to start tmux and type the command everytime. You can also create a bash or python script to execute automatically at start up or create systemd service.


8- Update you can also use systemd to enable interface

 I created file: like in the following location: /etc/systemd/system/django.service
Added the following

```sh
Unit
[Unit]
Description=django_port_8000
[Service]
ExecStart=/home/iradio/django.sh
PIDFile=/var/run/django_server.pid
Restart=always
RestartSec=30
[Install]
WantedBy=multi-user.target
```

django.sh contains:

```sh

#!/bin/bash
uwsgi /srv/http/uwsgi.ini

```


Note uwsgi.ini already included in repository might need to change locations ins uwsgi corresponding to your installation.
Also don't forget to install uwsgi  like  pip install uwsgi also make sure port 80 is free on your raspberry pi.

Also note when upgrading uwsgi might have issues, to resolve I usually uninstall with pip and then install again


# Usage

Functions can be accessed via the black menu on top, designed for latest browswers, older browsers will still see some sort of menu but not as nice.
## Play
To play selected radios.
## Add 
To add a file playlist or internet radio url, note should be mp3 type.

## Modify
To modify existing radio station.
## Delete
To delete existing radio station.
## Change Config
To change setting like homedirectory and transmitting frecuency.
## Export to csv
Added hability to export radio list to csv format so it can be used elsewhere like pyradio which I use a lot to listen to radios online also hability to download from site.


## Added api so you can interface with frontend frameworks and others
To check more details on the apis like parameters you can check api documentation on the server itself:

```sh

<hostname>/api/docs

In my case:
http://192.168.31.232/api/docs


```

![Alt Text](https://github.com/macunan/iradio/blob/main/api_docs.png)

## Also please support Django Ninja frameworks is awesome !
https://django-ninja.rest-framework.com
