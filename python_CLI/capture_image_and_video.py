#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 2023
@author: Sylvain Brisson sylvain.brisson@ens.fr
"""

import gphoto2 as gp
import os 
import datetime
import threading
import pyfakewebcam
import cv2
import numpy as np
import time


# Camera stuff

def capture_image(camera, dir="image"):
    
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    
    now = datetime.now()
    file_name = now.strftime("%Y-%m-%d_%H:%M:%S_.jpg")
    target = os.path.join(os.path.join(os.path.dirname(__file__),dir), file_name)
    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    print('Image captured and copied to : ', f"{dir}/{file_name}")

def camera_loop():
    
    global picture_commanded
    
    camera = gp.Camera()
    camera.init()
    
    fake_camera = pyfakewebcam.FakeWebcam('/dev/video2', 960, 640)
    
    last_capture_time = time.time()

    while True:
        
        # Capture image
        if picture_commanded:
            picture_commanded = False
            capture_image(camera)
        
        # Capture preview for livefeed
        file_data = camera.capture_preview()
        image_data = cv2.imdecode(np.frombuffer(file_data.get_data_and_size(), np.uint8), -1)
        # écriture de l'image sur le périphérique vidéo virtuel
        fake_camera.schedule_frame(image_data)
        
        # pause pour atteindre une fréquence de rafraîchissement cible de 1 FPS
        elapsed_time = time.time() - last_capture_time
        pause_time = max(0, 1 - elapsed_time)
        time.sleep(pause_time)
        last_capture_time = time.time()

       
def get_user_input():
    
    global picture_commanded
    
    while True :
        
        command = input("Appuyez sur une touche (q pour quitter, p pour prendre une photo) puis sur entrer: ")
        
        if command == 'p':
            picture_commanded = True

if __name__ == "__main__":
    
    # global variables
    picture_commanded = False
    
    # Créer les threads
    thread_command = threading.Thread(target=get_user_input)
    thread_camera = threading.Thread(target=camera_loop)

    # Démarrer les threads
    thread_command.start()
    thread_camera.start()

    # Attendre la fin des threads
    thread_command.join()
    thread_camera.join()