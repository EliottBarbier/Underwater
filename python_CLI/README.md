## Capture et lecture d'un flux video

La meilleure solution que j'ai trouvé et d'envoyer les frames capturées sur un port vidéo virtuel que l'on peut ensuite lire via gstreamer pour remonter le flux vidéo vers la surface. (NON TESTE)

Pour cela, sur la raspberry : 
```bash
# On créé le port vidéo virtuel
sudo modprobe v4l2loopback devices=1 video_nr=2 card_label="VirtualCam"
# Une fois un programme python de capture video lancé, on utilise gstreamer pour convertir le flux video en rtp et l'envoyer via udp sur l'ordinateur en surface
gst-launch-1.0 v4l2src device=/dev/video2 ! \
    queue ! \
    x264enc pass=qual quantizer=35 tune=zerolatency ! \
    rtph264pay ! \
    udpsink host=192.168.2.3 port=5000
```

Ensuite, on récupère le flux sur l'ordinateur de surface : 
```bash
gst-launch-1.0 -e -v udpsrc port=5000 ! \
	application/x-rtp, media=video, encoding-name=H264 ! \
	rtph264depay ! \
	queue ! \
	avdec_h264 ! \
	videoconvert ! \
	autovideosink
```