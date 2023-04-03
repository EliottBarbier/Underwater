#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 2023
@author: Sylvain Brisson sylvain.brisson@ens.fr
"""

import gphoto2 as gp
import cv2
import numpy as np
import pyfakewebcam
import time

# initialisation de la bibliothèque gphoto2
gp.check_result(gp.use_python_logging())
camera = gp.Camera()
camera.init()

# # configuration des paramètres de capture vidéo
# config = camera.get_config()
# print('Camera configuration:')
# for child in config.get_children():
#     print(child.get_label())

# activation du mode capture vidéo
# capture_target = config.get_child_by_name('capturetarget')
# capture_target.set_value('Memory card')
# camera.set_config(config)

# création d'un périphérique vidéo virtuel
# pour créer le périphérique video : sudo modprobe v4l2loopback devices=1 video_nr=2 card_label="VirtualCam"

fake_camera = pyfakewebcam.FakeWebcam('/dev/video2', 960, 640)

# capture vidéo et envoi au périphérique virtuel
last_capture_time = time.time()
while True:
    
    file_data = camera.capture_preview()
    image_data = cv2.imdecode(np.frombuffer(file_data.get_data_and_size(), np.uint8), -1)
    
    # affichage du flux vidéo via openCV
    cv2.imshow('Preview', image_data)
    if cv2.waitKey(1) == ord('q'):
        break
    
    # écriture de l'image sur le périphérique vidéo virtuel
    fake_camera.schedule_frame(image_data)
    
    # pause pour atteindre une fréquence de rafraîchissement cible de 1 FPS
    elapsed_time = time.time() - last_capture_time
    pause_time = max(0, 1 - elapsed_time)
    time.sleep(pause_time)
    last_capture_time = time.time()

# libération des ressources
cv2.destroyAllWindows()

camera.exit()

    