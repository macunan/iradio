## _Raspberry Pi FM Radio Transmitter_

![Alt Text](https://github.com/macunan/iradio/iradio.gif)


Iradio is browser based controller to transmitt FM radio from your Rasberry pi uses Django as front end and python together with the awesome RM Radio transmitter by Christophe Jaquet and Arch Linux Arm Branch https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3
and 
https://github.com/ChristopheJacquet/PiFmRds


## Requirements
-Linux Instalation running on Raspbery pi 3 board
-Small connector cable for GPIO 4 (pin 7 on header P1).
- A bit of time and effor
- Good power supply for your raspberry pi
- Fm Receiver so you can listen to your internet radio on or mp3s
- Computer or phone to follow all steps 
- ssh access your raspberry pi and root like user to execute backend commands
- Be careful with your country/state regulations regarding FM  transmissions is your responsibility to follow them and comply with local laws and regulations in your region.
## Installation

1-  I used Arch linux arm for my installation but I believe it can be any Linux as long as you have a recent kernel in my case 5.10.60-1-ARCH #1 SMP Sat Aug 21 14:56:38 UTC 2021 armv7l GNU/Linux it should be fine. Note only recent Kernel will function without issues, older kernel might work but you might face some issues.

2- 
```sh
Clone the source repository and run make in the src directory:

git clone https://github.com/ChristopheJacquet/PiFmRds.git
cd PiFmRds/src
make clean
make
```

Make sure you have all the required libraries and compilers installed  like gcc and python installed

If make reports no error (i.e. the pi_fm_rds executable gets generated), you can then simply run:
```sh
sudo ./pi_fm_rds
```
This will generate an FM transmission on 107.9 MHz, with default station name (PS), radiotext (RT) and PI-code, without audio. The radiofrequency signal is emitted on GPIO 4 (pin 7 on header P1).

You can add monophonic or stereophonic audio by referencing an audio file as follows:
```sh
sudo ./pi_fm_rds -audio sound.wav
```

Once compiled copy to your systems's bin directory in my case for Arch Linux:
```sh
/usr/local/bin
[root@mauripi bin]# ls -lhtr 

-rwxr-xr-x 1 root root  82K ago 26 18:56 pi_fm_rds


```

From there you should be to execute from any directory, note this should be executed by root like user.

I created a iradio user:
```sh
cat /etc/passwd
iradio:x:0:0:root:/home/iradio:/bin/bash
```

Once you are sure the latter is installed and transmitting correctly proceed with next step:

3-
Install sox in my OS command is pacman -S sox, also in ubuntu like systems it can be sudo apt-get install sox

Make sure sox is able to play local and remote streams
Example
```sh
sox  https://api.spreaker.com/listen/user/kgra/episode/latest/shoutcast.mp3
```
If you get any errors try a url that you know that works and try again if not you might need to compile sox from source.

4- Install Python and Django and tmux

-Install Python and Python installer
```sh
pacman -S python python-pip tmux
```
-Install Django
```sh
pip install django
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
ExecStart=/home/iradio/radio.sh
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
Note the service will use /home/iradio/radio.sh to start and stop the radio, the file
looks like the following:
```sh
#!/bin/bash
sox -t mp3 https://api.spreaker.com/listen/user/kgra/episode/latest/shoutcast.mp3 -t wav - |pi_fm_rds -freq  91.5.0 -audio -
 ```

You might need to edit line 17 of 
https://github.com/macunan/iradio/blob/main/fmtrans/pyfunctions.py
```sh
  file = open(r"/home/iradio/radio.sh", "w") 
```
and add the proper location  radio.sh  because the class will create a new radio.sh every time the radio is activated via the frontend, afterwards systemctl start iradio.service is executed.
Also you might need to modify line 13 of pyfunctions and change the correct frecuency -freq
by default is 91.5 but that might need to change in you local case. Also you can create a iradio like user with root user like shown above.

```sh
  end=" -t wav - |pi_fm_rds -freq  91.5.0 -audio -"
```




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





Iradio is browser based controller to transmitt FM radio from your Rasberry pi uses Django as front end and python together with the awesome RM Radio transmitter by Christophe Jaquet and Arch Linux Arm Branch https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3
and 
https://github.com/ChristopheJacquet/PiFmRds


## Requirements
-Linux Instalation running on Raspbery pi 3 board
-Small connector cable for GPIO 4 (pin 7 on header P1).
- A bit of time and effor
- Good power supply for your raspberry pi
- Fm Receiver so you can listen to your internet radio on or mp3s
- Computer or phone to follow all steps 
- ssh access your raspberry pi and root like user to execute backend commands
- Be careful with your country/state regulations regarding FM  transmissions is your responsibility to follow them and comply with local laws and regulations in your region.
## Installation

1-  I used Arch linux arm for my installation but I believe it can be any Linux as long as you have a recent kernel in my case 5.10.60-1-ARCH #1 SMP Sat Aug 21 14:56:38 UTC 2021 armv7l GNU/Linux it should be fine. Note only recent Kernel will function without issues, older kernel might work but you might face some issues.

2- 
```sh
Clone the source repository and run make in the src directory:

git clone https://github.com/ChristopheJacquet/PiFmRds.git
cd PiFmRds/src
make clean
make
```

Make sure you have all the required libraries and compilers installed  like gcc and python installed

If make reports no error (i.e. the pi_fm_rds executable gets generated), you can then simply run:
```sh
sudo ./pi_fm_rds
```
This will generate an FM transmission on 107.9 MHz, with default station name (PS), radiotext (RT) and PI-code, without audio. The radiofrequency signal is emitted on GPIO 4 (pin 7 on header P1).

You can add monophonic or stereophonic audio by referencing an audio file as follows:
```sh
sudo ./pi_fm_rds -audio sound.wav
```

Once compiled copy to your systems's bin directory in my case for Arch Linux:
```sh
/usr/local/bin
[root@mauripi bin]# ls -lhtr 

-rwxr-xr-x 1 root root  82K ago 26 18:56 pi_fm_rds


```

From there you should be to execute from any directory, note this should be executed by root like user.

I created a iradio user:
```sh
cat /etc/passwd
iradio:x:0:0:root:/home/iradio:/bin/bash
```

Once you are sure the latter is installed and transmitting correctly proceed with next step:

3-
Install sox in my OS command is pacman -S sox, also in ubuntu like systems it can be sudo apt-get install sox

Make sure sox is able to play local and remote streams
Example
```sh
sox  https://api.spreaker.com/listen/user/kgra/episode/latest/shoutcast.mp3
```
If you get any errors try a url that you know that works and try again if not you might need to compile sox from source.

4- Install Python and Django and tmux

-Install Python and Python installer
```sh
pacman -S python python-pip tmux
```
-Install Django
```sh
pip install django
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
ExecStart=/home/iradio/radio.sh
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
Note the service will use /home/iradio/radio.sh to start and stop the radio, the file
looks like the following:
```sh
#!/bin/bash
sox -t mp3 https://api.spreaker.com/listen/user/kgra/episode/latest/shoutcast.mp3 -t wav - |pi_fm_rds -freq  91.5.0 -audio -
 ```

You might need to edit line 17 of 
https://github.com/macunan/iradio/blob/main/fmtrans/pyfunctions.py
```sh
  file = open(r"/home/iradio/radio.sh", "w") 
```
and add the proper location  radio.sh  because the class will create a new radio.sh every time the radio is activated via the frontend, afterwards systemctl start iradio.service is executed.
Also you might need to modify line 13 of pyfunctions and change the correct frecuency -freq
by default is 91.5 but that might need to change in you local case. Also you can create a iradio like user with root user like shown above.

```sh
  end=" -t wav - |pi_fm_rds -freq  91.5.0 -audio -"
```




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


