def start_controller_loop(queue):
    while not queue.empty():
        print(queue.get())
