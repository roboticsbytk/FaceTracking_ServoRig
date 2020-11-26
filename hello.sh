#!/bin/bash
sudo chmod a+rw /dev/ttyACM0

#sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2
ps aux | grep '/usr/lib/gvfs/gvfsd-gphoto2 --spawner :1.22 /org/gtk/gvfs/exec_spaw/1'

PID=$(ps aux | grep "/usr/lib/gvfs/gvfsd-[g]photo2 --spawner :1.22 /org/gtk/gvfs/exec_spaw/1" | awk '{print $2}')
echo "$PID"
kill -9 $PID

ps aux | grep '/usr/lib/gvfs/gvfsd-gphoto2 --spawner :1.22 /org/gtk/gvfs/exec_spaw/1'


gphoto2  --set-config flashmode=2   --stdout --capture-movie | ffmpeg -i  pipe:0  -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video1
