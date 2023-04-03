#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 2023
@author: Sylvain Brisson sylvain.brisson@ens.fr
"""

import logging
import locale
import os
import argparse
from datetime import datetime

import gphoto2 as gp

def get_camera():
    camera = gp.Camera()
    camera.init()
    return camera
    
def capture_image(camera, name, dir):
    
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    now = datetime.now()
    target = os.path.join(os.path.join(os.path.dirname(__file__),dir), now.strftime("%Y-%m-%d_%H:%M:%S_")+name+".jpg")
    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    print('Image captured and copied to : ', target)

if __name__ == "__main__":
    
    # set logging
    locale.setlocale(locale.LC_ALL, '')
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())  
    
    # parse command line args
    # parsing arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='name to give to the picture (without extension)', nargs="?", default="capt")
    parser.add_argument('-d', dest="dest_dir",type=str, help='directory in which to save picture', nargs="?", default=".")
    args = parser.parse_args()     
        
    # init camera
    camera = get_camera()
    
    # take picture
    capture_image(camera, args.file_name, args.dest_dir)