import threading
import time

class workerThread(threading.Thread):
    
    def __init__(self, id, guard_duty:threading.Lock):
        super().__init__()
        self.id = id
        self.guard_duty = guard_duty

    def run(self):
        print("I'm running thread #", self.id)
        self.guard_duty.acquire()
        print("On guard duty", self.id)
        time.sleep(5)
        print("I'm off duty", self.id)
        self.guard_duty.release()
        print("I'm done running thread #", self.id)

        

def main():

    print("Main Thread Start")

    guard_duty = threading.Lock()

    t1 = workerThread(1, guard_duty)
    t2 = workerThread(2, guard_duty)
    t3 = workerThread(3, guard_duty)
    
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()



if __name__ == '__main__':
    main()

