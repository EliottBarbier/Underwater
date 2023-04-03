gst-launch-1.0 -e -v udpsrc port=5000 ! \
	application/x-rtp, media=video, encoding-name=H264 ! \
	rtph264depay ! \
	queue ! \
	avdec_h264 ! \
	videoconvert ! \
	autovideosink