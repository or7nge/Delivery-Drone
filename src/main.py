from multiprocessing import Process, Queue
from camera.camera import start_camera_loop
from controller.controller import start_controller_loop
from config import *

if __name__ == '__main__':
    queue = Queue()
    camera_thread = Process(target=start_camera_loop, args=(queue,))
    # controller_thread = Process(target=start_controller_loop, args=(queue,))
    camera_thread.start()
    # controller_thread.start()
    camera_thread.join()
    # controller_thread.join()
