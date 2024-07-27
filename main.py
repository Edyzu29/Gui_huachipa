from script import *
from interfaz import *
#from build.gui import *

import tkinter as tk
import tkinter.font as tkFont

actual_path = "D:\\fotos huachipa"

camaras = ["Camara1", "Camara2"]

camara_sort = ["Camara1_sort", "Camara2_sort"]

Estaciones = ['CA_HU_04 Paraiso', 'CA-HU-01 Nieveria', 'CA-HU-09 Santa Maria']




if __name__ == "__main__":

    for estation in Estaciones:

        stacion_path = os.path.join(actual_path, estation)

        for index in range(0,2):

            image_paths = os.path.join(stacion_path, camaras[index])

            destini_photos = os.path.join(stacion_path, camara_sort[index])

            if os.path.isdir(image_paths):
        
                sort_img(image_paths, destini_photos)

                reformart(destini_photos)

                delete_empty_folders(destini_photos)

                make_video(destini_photos)

            else:
                
                continue