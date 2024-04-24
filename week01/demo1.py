from cse251 import *
import threading

print ("Hello world")



def func(par1):
    print("before", par1)
    time.sleep(3)
    print("after", par1)



t1 = threading.Thread(target=func,args=(1,))
t2 = threading.Thread(target=func,args=(2,))

t1.start()
t2.start()

t1.join()
t2.join()

