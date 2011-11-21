import mapper
import os
import Tkinter
from Queue import Empty
from multiprocessing import Process, Queue
from threading import Thread


def f(q,on_list):
    import Tkinter
    def tcall(b_num):
        temp_str=tbox.get()
        q.put((b_num,temp_str))
        
    def onquit():
        q.put("quit")
        root.quit()

    root = Tkinter.Tk()
    tbox=Tkinter.Entry(root)
    tbox.pack()
    quit_button = Tkinter.Button(root, text="Quit", command=lambda: onquit())
    
    quit_button.pack()
    command_button={}
    for bd_num in on_list:
        txt_str=("Enter command for Board " + str(bd_num))
        def tc(b):
            return lambda: tcall(b)
        command_button[bd_num] = Tkinter.Button(root, text=txt_str,command=tc(bd_num))
        command_button[bd_num].pack()
        print ("command button" ,command_button)

    #command2_button = Tkinter.Button(root, text="Enter command",
     #                               command=lambda: tcall(2))
    #command2_button.pack()

    
    root.mainloop()


          

OS = os.name
#Open Serial Port to Read Data
if OS == 'nt':
    port_list = [14-1,5-1]
elif OS == 'posix':
    import sys
    sys.path.append("/Users/mahtab-ghamsari/Projects/Mappings/pyserial-2.5/")
    port_list=['/dev/tty.usbserial-A8004lV1','/dev/tty.usbserial-AD004lUY']

from fungible_board_class import Fungible_Node
print Fungible_Node
still_alive=1    

#root.after(5, ontimer)
#root.mainloop()

m_inst= mapper.device("Fungible1", 9000)
b_array={}
b_num=0
b_list=[0,1]
open_list=[]
for b_num in b_list:
    try:
        b_array[b_num]=Fungible_Node(port_list[b_num],115200,0.3,m_inst)
        open_list.append(b_num)
    except:
        raise


try:
    q = Queue()
    print q

    if OS == 'nt':
        p = Thread(target=f, args=(q,open_list,))

    elif self.OS == 'posix':
        p = Process(target=f, args=(q,open_list,))
except:
    print ("Thread couldn't initialize")
            
try:
    p.start()
except:
    print("Thread couldn't start")
    raise


#board3=Fungible_Node(port_list[1],115200,0.3,m_inst)

#while ((b_array[0].quit==0) and (b_array[1].quit==0)):
try:  
    while (still_alive==1):
        try:
            for b_num in open_list:

                b_array[b_num].get_serial_data()
                b_array[b_num].update_mapper_signals()
                b_array[b_num].poll(m_inst)
        except:
            print("can't read write signals")
            raise
        try:
            queue_list=q.get_nowait()    # prints "[42, None, 'hello']"
            print ("queue list: ", queue_list)
            if queue_list=="quit":
                still_alive=0
                break              
                    
            else:
                if (queue_list[0] in open_list):
                    if queue_list[1].startswith('Sb'):
                        input_mode = queue_list
                    elif queue_list[1].startswith('SI'):
                        get_board_number = 1
                        
                    #print("waiting",ser.inWaiting())
                    #ser.flushInput()
                    print("push to com: ", queue_list[0])
                    print(repr(queue_list[1]+"\r"))
                    
                   # ser.flushInput()
    #                b_array[0].s_write(queue_list+"\r")
                    b_array[queue_list[0]].s_write(queue_list[1]+"\r")
    #                still_alive=0
                    #break  
                    #buff_read()
            #            print "Contents of Serial Buffer", s
        #        else:
                continue
                
        except Empty:
            pass
except KeyboardInterrupt:
    pass
print ("auto-closing")
for b_num in open_list:
    try:
        b_array[b_num].close_nicely()
    except:
        print ("board ", b_num, "already closed (or just plain couldn't close)!") 

p.join()
