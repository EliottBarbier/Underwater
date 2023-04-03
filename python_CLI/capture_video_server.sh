gst-launch-1.0 v4l2src device=/dev/video2 ! \
    queue ! \
    x264enc pass=qual quantizer=35 tune=zerolatency ! \
    rtph264pay ! \
    udpsink host=192.168.2.3 port=5000