from PIL import Image
import imageio
import cv2
import os
import numpy as np
import pyopencl as cl
from tqdm import tqdm
import re

# Configurar PyOpenCL para usar la GPU AMD
platforms = cl.get_platforms()
devices = platforms[0].get_devices(cl.device_type.GPU)
context = cl.Context(devices)
queue = cl.CommandQueue(context)

def cambiar_extension(directorio, extension_vieja, extension_nueva):
    # Lista todos los archivos en el directorio
    for nombre_archivo in os.listdir(directorio):
        # Verifica si el archivo tiene la extensión vieja
        if nombre_archivo.lower().endswith(extension_vieja.lower()):
            # Construye las rutas de origen y destino
            nombre_archivo_sin_extension = os.path.splitext(nombre_archivo)[0]
            nombre_archivo_nuevo = nombre_archivo_sin_extension + extension_nueva
            ruta_origen = os.path.join(directorio, nombre_archivo)
            ruta_destino = os.path.join(directorio, nombre_archivo_nuevo)
            
            # Renombra el archivo
            os.rename(ruta_origen, ruta_destino)

def sort_img(image_paths, stacion_path):

    file_names = os.listdir(image_paths)

    img_mouth = list(set([str(x[0:2]) for x in file_names]))
    img_days = list(set([str(x[2:4]) for x in file_names]))

    img_files = os.listdir(image_paths)

    for mouth in img_mouth:
        for day in img_days:

            img_name = mouth + day

            dir_path = os.path.join(stacion_path, img_name)
            
            os.makedirs(dir_path, exist_ok=True)

            for img in img_files:
                if img.startswith(img_name):
                    og_path = os.path.join(image_paths, img)
                    dt_path = os.path.join(dir_path, img)
                    os.rename(og_path, dt_path)

def reformart(stacion_path):

    for subdir in os.listdir(stacion_path):

        subdir_subdir = os.path.join(stacion_path, subdir)

        cambiar_extension(subdir_subdir, '.JPG', '.jpg')

def load_images(image_paths):
    images = []

    img_name = [img for img in os.listdir(image_paths) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]

    images = [cv2.imread(os.path.join(image_paths, img)) for img in img_name]

    return images

def process_images(images):
    processed_images = []
    for img in tqdm(images, desc="Procesando imágenes"):

        img_buf = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=img)
        kernel_code = """
        __kernel void invert(__global uchar *img) {
            int i = get_global_id(0);
            img[i] = 255 - img[i];
        }
        """
        program = cl.Program(context, kernel_code).build()
        program.invert(queue, img.shape, None, img_buf)
        processed_img = np.empty_like(img)
        cl.enqueue_copy(queue, processed_img, img_buf).wait()
        processed_images.append(processed_img)
    return processed_images

def create_video(images, output_path, fps=30):
    height, width, layers = images[0].shape
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for img in tqdm(images, desc="Creando video"):
        video.write(img)
    video.release()

def make_gift(stacion_path):

    for subdir in os.listdir(stacion_path):

        subdir_subdir = os.path.join(stacion_path, subdir)

        img_name = [img for img in os.listdir(subdir_subdir) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        img_load = [Image.open(os.path.join(subdir_subdir, img)) for img in img_name]

        git_path = os.path.join(stacion_path, f"{subdir}.gif")

        with imageio.get_writer(git_path, mode='I', format='gif', duration=100) as writer:
            for frame in img_load:
                # frame = frame.convert('RGB')
                # writer.append_data(np.array(frame))
                writer.append_data(frame)

def make_video(stacion_path):

    for subdir in os.listdir(stacion_path):

        if '.' not in subdir:

            subdir_subdir = os.path.join(stacion_path, subdir)

            images = load_images(subdir_subdir)

            processed_images = process_images(images)

            output_gif_path = os.path.join(stacion_path, subdir + ".mp4")

            create_video(processed_images, output_gif_path, fps=4)

            print( "video create: " + subdir + ".mp4")


        else:

            continue


def delete_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
                print(f"Carpeta vacía eliminada: {dir_path}")
            except OSError as e:
                print(f"No se pudo eliminar la carpeta: {dir_path} - {e}")
