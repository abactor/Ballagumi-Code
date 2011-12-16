import mapper
import os
import Tkinter
from Queue import Empty
from multiprocessing import Process, Queue
from threading import Thread



def main_loop():
  
#        while (still_alive==1):

           # f(q,open_list)
    
    for b_num in open_list:

        try:
            b_array[b_num].get_serial_data()
            b_array[b_num].update_mapper_signals()
            b_array[b_num].poll(m_inst)
        except:
            print("trying to get/update board",b_num)
            print("can't read write signals")
            #raise
    try:
        
        queue_list=q.get_nowait()    # prints "[42, None, 'hello']"
        print ("queue list: ", queue_list)
        if queue_list=="quit":
            still_alive=0
            #break
            return
                
        else:
            if (queue_list[0] in open_list):
                print("push to com: ", queue_list[0])
                print(repr(queue_list[1]+"\r"))
                if queue_list[1].startswith('Sb'):
                    input_mode = queue_list
                elif queue_list[1].startswith('SI'):
                    get_board_number = 1
               # else:
                   # ser_stream=(b_array[queue_list[0]].s_read(10))
                   # for ser_line in ser_stream:
                   #     print(ser_line)
                    
                #print("waiting",ser.inWaiting())
                #ser.flushInput()
                
                
               # ser.flushInput()
#                b_array[0].s_write(queue_list+"\r")
                b_array[queue_list[0]].s_write(queue_list[1]+"\r")
                
                print ("in waiting ", b_array[queue_list[0]].ser.inWaiting())
                ser_stream=(b_array[queue_list[0]].s_read(10))
                print ("ser stream: ", ser_stream)
                for ser_line in ser_stream:
                    print("Returned : ",ser_line)
    #                still_alive=0
                #break  
                #buff_read()
        #            print "Contents of Serial Buffer", s
    #        else:
            #continue
            return
       
    #except KeyboardInterrupt:
    except:
        
        pass
    #end main_loop

def f(q,on_list):
    import Tkinter
    def tcall(b_num):
        temp_str=tbox.get()
        q.put((b_num,temp_str))
        
    def onquit():
        q.put("quit")
        root.quit()
    print "in gui"
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
    def ontimer():
        #print 'someshit'
        main_loop()
  #                  check the serial port
        root.after(1, ontimer)
    
    ontimer()
    #root.after(500, ontimer)
    root.mainloop()
          

OS = os.name
#Open Serial Port to Read Data
if OS == 'nt':
    port_list = [14-1,5-1,6-1]
elif OS == 'posix':
    import sys
    sys.path.append("/Users/mahtab-ghamsari/Projects/Mappings/pyserial-2.5/")
    port_list=['/dev/tty.usbserial-A8004lV1','/dev/tty.usbserial-AD004lUY']

from fungible_board_class import Fungible_Node
print Fungible_Node


#root.after(5, ontimer)
#root.mainloop()

m_inst= mapper.device("Fungible1", 9000)
b_array={}
b_num=0
b_list=[0,1,2]
open_list=[]
for b_num in b_list:
    try:
        b_array[b_num]=Fungible_Node(port_list[b_num],115200,0.3,m_inst)
        open_list.append(b_num)
    except:
        print ("error on b_num",b_num, port_list[b_num])
        raise


try:
    q = Queue()
    print q

#    if OS == 'nt':
 #       p = Thread(target=f, args=(q,open_list,))

#    elif self.OS == 'posix':
#        p = Process(target=f, args=(q,open_list,))
except:
    print ("Queue couldn't open")
            
#try:
    #p.start()
try:    
    f(q,open_list)
except:
    
    print("GUI couldn't start")
    #raise


#board3=Fungible_Node(port_list[1],115200,0.3,m_inst)

#while ((b_array[0].quit==0) and (b_array[1].quit==0)):

print ("auto-closing")
for b_num in open_list:
    try:
        b_array[b_num].close_nicely()
    except:
        print ("board ", b_num, "already closed (or just plain couldn't close)!") 

#p.join()
