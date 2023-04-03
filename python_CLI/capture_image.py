#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 2023
@author: Sylvain Brisson sylvain.brisson@ens.fr
"""

import logging
import locale
import os
import sys
import argparse
from datetime import datetime
from re import A
from multiprocessing.pool import ThreadPool

import gphoto2 as gp
   
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
     
#init list of camera
locale.setlocale(locale.LC_ALL, '')
if len(sys.argv) > 2:
    print('Usage: {} [port_address]'.format(sys.argv[0]))
logging.basicConfig(
    format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
callback_obj = gp.check_result(gp.use_python_logging())
if len(sys.argv) > 1:
    # if user has given an address open it directly
    addr = sys.argv[1]
else:
    # make a list of all available cameras
    camera_list = list(gp.Camera.autodetect())
    if not camera_list:
        print('No camera detected')
    camera_list.sort(key=lambda x: x[0])
    port_info_list = gp.PortInfoList()
    port_info_list.load()
    abilities_list = gp.CameraAbilitiesList()
    abilities_list.load()
    camera_list = abilities_list.detect(port_info_list)



def get_cameras(camera_list):
    cameras = []
    for i in range(len(camera_list)):
        addr = camera_list[i][1] 
        camera = gp.Camera()
        idx = port_info_list.lookup_path(addr)
        camera.set_port_info(port_info_list[idx])
        idx = abilities_list.lookup_model(camera_list[0][0])
        camera.set_abilities(abilities_list[idx])
        cameras.append(camera)
    return cameras


cameras = get_cameras(camera_list)

def capture_image(i, name = args.file_name, dir = args.dest_dir, cameras = cameras):
    file_path = cameras[i].capture(gp.GP_CAPTURE_IMAGE)
    now = datetime.now()
    target = os.path.join(os.path.join(os.path.dirname(__file__),dir), now.strftime(f"%Y-%m-%d_%H:%M:%S_{i}")+name+".jpg")
    camera_file = cameras[i].file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    print('Image captured and copied to : ', target, 'for camera_1')


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
     
    #init list of camera
    locale.setlocale(locale.LC_ALL, '')
    if len(sys.argv) > 2:
        print('Usage: {} [port_address]'.format(sys.argv[0]))
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())
    if len(sys.argv) > 1:
        # if user has given an address open it directly
        addr = sys.argv[1]
    else:
        # make a list of all available cameras
        camera_list = list(gp.Camera.autodetect())
        if not camera_list:
            print('No camera detected')
        camera_list.sort(key=lambda x: x[0])
        port_info_list = gp.PortInfoList()
        port_info_list.load()
        abilities_list = gp.CameraAbilitiesList()
        abilities_list.load()
        camera_list = abilities_list.detect(port_info_list)
    
    # take picture
    with ThreadPool() as pool:
        pool.map(capture_image, range(2))

    # init camera
    cameras = get_cameras(camera_list)


