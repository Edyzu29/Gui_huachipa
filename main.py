from script import *
from interfaz import *
#from build.gui import *

import tkinter as tk
import tkinter.font as tkFont

actual_path = "D:\\fotos huachipa"

camaras = ["Camara1", "Camara2"]

camara_sort = ["Camara1_sort", "Camara2_sort"]

stacion_path = os.path.join(actual_path, 'CA-HU-09 Santa Maria')



if __name__ == "__main__":

    # for index in range(0,2):

    #     image_paths = os.path.join(stacion_path, camaras[index])

    #     destini_photos = os.path.join(stacion_path, camara_sort[index])
    
    #     # sort_img(image_paths, destini_photos)

    #     # reformart(destini_photos)

    #     # delete_empty_folders(destini_photos)

    #     make_video(destini_photos)
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get the list of available font families
    available_fonts = tkFont.families()

    # Print the available fonts
    print("Available fonts:")
    for font in available_fonts:
        print(font)

    root.destroy()
