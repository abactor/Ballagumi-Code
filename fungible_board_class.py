import sys
import os
import serial
import mapper
import string
import time
        
from multiprocessing import Process, Queue
from threading import Thread
from Queue import Empty
import time


sensorinfo = [(1, '0S1', 'LeftBase', 'A', 'ON'),
              (1, '1S1', 'LeftBase', 'B', 'ON'),
              (1, '2S1', 'LeftBase', 'C', 'ON'),
              (1, '3S1', 'LeftWingBend', '1', 'ON'),
              (1, '4S1', 'LeftWingBend', '2', 'ON'),
              (1, '5S1', 'LeftWingBend', '3', 'ON'),
              (1, '6S1', 'LeftWingBend', '4', 'ON'),
              (1, '7S1', 'Horizontal', '1', 'ON'),
              (1, '0D1', 'LeftBase', 'A-B', 'ON'),
              (1, '1D1', 'LeftBase', 'A-C', 'ON'),
              (1, '2D1', 'instr1', 'NA', 'ON'),
              (1, '3D1', 'instr2', 'NA', 'ON'),
              (1, '4D1', 'N-A1', 'NA', 'ON'),
              (1, '5D1', 'N-A2', 'NA', 'ON'),
              (1, '6D1', 'N-A3', 'NA', 'ON'),
              (1, '7D1', 'N-A4', 'NA', 'ON'),

              (1, '0S0', 'LeftBase', 'A', 'OFF'),
              (1, '1S0', 'LeftBase', 'B', 'OFF'),
              (1, '2S0', 'LeftBase', 'C', 'OFF'),
              (1, '3S0', 'LeftWingBend', '1', 'OFF'),
              (1, '4S0', 'LeftWingBend', '2', 'OFF'),
              (1, '5S0', 'LeftWingBend', '3', 'OFF'),
              (1, '6S0', 'LeftWingBend', '4', 'OFF'),
              (1, '7S0', 'Horizontal', '1', 'OFF'),
              (1, '0D0', 'LeftBase', 'A-B', 'OFF'),
              (1, '1D0', 'LeftBase', 'A-C', 'OFF'),
              (1, '2D0', 'instr1', 'NA', 'OFF'),
              (1, '3D0', 'instr2', 'NA', 'OFF'),
              (1, '4D0', 'N-A1', 'NA', 'OFF'),
              (1, '5D0', 'N-A2', 'NA', 'OFF'),
              (1, '6D0', 'N-A3', 'NA', 'OFF'),
              (1, '7D0', 'N-A4', 'NA', 'OFF'),

              (2, '0S1', 'LeftMid', 'A', 'ON'),
              (2, '1S1', 'LeftMid', 'B', 'ON'),
              (2, '2S1', 'LeftMid', 'C', 'ON'),
              (2, '3S1', 'LeftTip', 'A', 'ON'),
              (2, '4S1', 'LeftTip', 'B', 'ON'),
              (2, '5S1', 'Horizontal', '2', 'ON'),
              (2, '6S1', 'Horizontal', '3', 'ON'),
              (2, '7S1', 'Horizontal', '4', 'ON'),
              (2, '0D1', 'LeftMid', 'A-B', 'ON'),
              (2, '1D1', 'LeftMid', 'A-C', 'ON'),
              (2, '2D1', 'instr1', 'NA', 'ON'),
              (2, '3D1', 'instr2', 'NA', 'ON'),
              (2, '4D1', 'LeftTip-HorizontalBend', 'NA', 'ON'),
              (2, '5D1', 'LeftTip', 'B-A', 'ON'),
              (2, '6D1', 'LeftTip-LeftMid', 'NA', 'ON'),
              (2, '7D1', 'Horizontal_Bend', '3-4', 'ON'),

              (2, '0S0', 'LeftMid', 'A', 'OFF'),
              (2, '1S0', 'LeftMid', 'B', 'OFF'),
              (2, '2S0', 'LeftMid', 'C', 'OFF'),
              (2, '3S0', 'LeftTip', 'A', 'OFF'),
              (2, '4S0', 'LeftTip', 'B', 'OFF'),
              (2, '5S0', 'Horizontal', '2', 'OFF'),
              (2, '6S0', 'Horizontal', '3', 'OFF'),
              (2, '7S0', 'Horizontal', '4', 'OFF'),
              (2, '0D0', 'LeftMid', 'A-B', 'OFF'),
              (2, '1D0', 'LeftMid', 'A-C', 'OFF'),
              (2, '2D0', 'instr1', 'NA', 'OFF'),
              (2, '3D0', 'instr2', 'NA', 'OFF'),
              (2, '4D0', 'LeftTip-HorizontalBend', 'NA', 'OFF'),
              (2, '5D0', 'LeftTip', 'B-A', 'OFF'),
              (2, '6D0', 'LeftTip-LeftMid', 'NA', 'OFF'),
              (2, '7D0', 'Horizontal_Bend', '3-4', 'OFF'),

              (3, '0S1', 'RightBase', 'A', 'ON'),
              (3, '1S1', 'RightBase', 'B', 'ON'),
              (3, '2S1', 'RightBase', 'C', 'ON'),
              (3, '3S1', 'RightWingBend', '1', 'ON'),
              (3, '4S1', 'RightWingBend', '2', 'ON'),
              (3, '5S1', 'RightWingBend', '3', 'ON'),
              (3, '6S1', 'RightWingBend', '4', 'ON'),
              (3, '7S1', 'VerticalBend', '2', 'ON'),
              (3, '0D1', 'RightBase', 'A-B', 'ON'),
              (3, '1D1', 'RightBase', 'A-C', 'ON'),
              (3, '2D1', 'RightWingBend', '2-3', 'ON'),
              (3, '3D1', 'RightWingBend', '1-2', 'ON'),
              (3, '4D1', 'RightBase-RightWingBend', 'NA', 'ON'),
              (3, '5D1', 'RightWingBend-VerticalBend', 'NA', 'ON'),
              (3, '6D1', 'instr1', 'NA', 'ON'),
              (3, '7D1', 'instr2', 'NA', 'ON'),

              (3, '0S0', 'RightBase', 'A', 'OFF'),
              (3, '1S0', 'RightBase', 'B', 'OFF'),
              (3, '2S0', 'RightBase', 'C', 'OFF'),
              (3, '3S0', 'RightWingBend', '1', 'OFF'),
              (3, '4S0', 'RightWingBend', '2', 'OFF'),
              (3, '5S0', 'RightWingBend', '3', 'OFF'),
              (3, '6S0', 'RightWingBend', '4', 'OFF'),
              (3, '7S0', 'VerticalBend', '2', 'OFF'),
              (3, '0D0', 'RightBase', 'A-B', 'OFF'),
              (3, '1D0', 'RightBase', 'A-C', 'OFF'),
              (3, '2D0', 'RightWingBend', '2-3', 'OFF'),
              (3, '3D0', 'RightWingBend', '1-2', 'OFF'),
              (3, '4D0', 'RightBase-RightWingBend', 'NA', 'OFF'),
              (3, '5D0', 'RightWingBend-VerticalBend', 'NA', 'OFF'),
              (3, '6D0', 'instr1', 'NA', 'OFF'),
              (3, '7D0', 'instr2', 'NA', 'OFF'),

              (1, '0S2', 'LeftBase', 'A', 'COMP'),
              (1, '1S2', 'LeftBase', 'B', 'COMP'),
              (1, '2S2', 'LeftBase', 'C', 'COMP'),
              (1, '3S2', 'LeftWingBend', '1', 'COMP'),
              (1, '4S2', 'LeftWingBend', '2', 'COMP'),
              (1, '5S2', 'LeftWingBend', '3', 'COMP'),
              (1, '6S2', 'LeftWingBend', '4', 'COMP'),
              (1, '7S2', 'Horizontal', '1', 'COMP'),
              (1, '0D2', 'LeftBase', 'A-B', 'COMP'),
              (1, '1D2', 'LeftBase', 'A-C', 'COMP'),
              (1, '2D2', 'instr1', 'NA', 'COMP'),
              (1, '3D2', 'instr2', 'NA', 'COMP'),
              (1, '4D2', 'N-A1', 'NA', 'COMP'),
              (1, '5D2', 'N-A2', 'NA', 'COMP'),
              (1, '6D2', 'N-A3', 'NA', 'COMP'),
              (1, '7D2', 'N-A4', 'NA', 'COMP'),

             

              (2, '0S2', 'LeftMid', 'A', 'COMP'),
              (2, '1S2', 'LeftMid', 'B', 'COMP'),
              (2, '2S2', 'LeftMid', 'C', 'COMP'),
              (2, '3S2', 'LeftTip', 'A', 'COMP'),
              (2, '4S2', 'LeftTip', 'B', 'COMP'),
              (2, '5S2', 'Horizontal', '2', 'COMP'),
              (2, '6S2', 'Horizontal', '3', 'COMP'),
              (2, '7S2', 'Horizontal', '4', 'COMP'),
              (2, '0D2', 'LeftMid', 'A-B', 'COMP'),
              (2, '1D2', 'LeftMid', 'A-C', 'COMP'),
              (2, '2D2', 'instr1', 'NA', 'COMP'),
              (2, '3D2', 'instr2', 'NA', 'COMP'),
              (2, '4D2', 'LeftTip-HorizontalBend', 'NA', 'COMP'),
              (2, '5D2', 'LeftTip', 'B-A', 'COMP'),
              (2, '6D2', 'LeftTip-LeftMid', 'NA', 'COMP'),
              (2, '7D2', 'Horizontal_Bend', '3-4', 'COMP'),

             

              (3, '0S2', 'RightBase', 'A', 'COMP'),
              (3, '1S2', 'RightBase', 'B', 'COMP'),
              (3, '2S2', 'RightBase', 'C', 'COMP'),
              (3, '3S2', 'RightWingBend', '1', 'COMP'),
              (3, '4S2', 'RightWingBend', '2', 'COMP'),
              (3, '5S2', 'RightWingBend', '3', 'COMP'),
              (3, '6S2', 'RightWingBend', '4', 'COMP'),
              (3, '7S2', 'VerticalBend', '2', 'COMP'),
              (3, '0D2', 'RightBase', 'A-B', 'COMP'),
              (3, '1D2', 'RightBase', 'A-C', 'COMP'),
              (3, '2D2', 'RightWingBend', '2-3', 'COMP'),
              (3, '3D2', 'RightWingBend', '1-2', 'COMP'),
              (3, '4D2', 'RightBase-RightWingBend', 'NA', 'COMP'),
              (3, '5D2', 'RightWingBend-VerticalBend', 'NA', 'COMP'),
              (3, '6D2', 'instr1', 'NA', 'COMP'),
              (3, '7D2', 'instr2', 'NA', 'COMP')]


class Fungible_Node:
  
    def __init__(self,port_num,baud,t_out, m_inst):
        self.quit=0
        print "Starting Fungible Initialization"
        try:
            self.OS = os.name   
            self.inBuffer=""
            self.port_num=port_num
            print self.port_num
            self.baud=baud
            print self.baud
            self.t_out=t_out
            print self.t_out
            self.open_connection()
            print ("Connection opened",self.ser)
            self.temp_buff=""
           # self.q = Queue()
           # print self.q

            #try:
             #   if self.OS == 'nt':
              #      print __name__
#                    self.p = Thread(target=self.f, args=(self.q,))

               # elif self.OS == 'posix':
                    #self.p = Process(target=self.f, args=(self.q,))

                #print self.pNoneType
            #except:
                #print ("Thread couldn't initialize")
            
            #try:
                #self.p.start()
            #except:
            #    print("Thread couldn't start")
             #   raise
            self.addr=0
            print ("Try to get i2c addr")
            while (self.addr<1):
                self.get_i2c_address()
                
                
            print ("I2C_address:",self.addr)
            self.pairs={}
            item_num=0
            self.number_of_sigs=0
            self.sig_names={}
            self.info_index={}
            self.state=0

            print ("Try to get sig info")  
            while (len(self.sig_names)<1):
                self.get_signal_info()
                time.sleep(1)
            
            print("sig names attained: ",self.sig_names)
            self.serial_sigs={}
            self.old_s_sigs={}
            self.mapper_sigs={}
       

            self.create_mapper_signals(m_inst)
            self.s_write("Sc 5\r")
            time.sleep(1)
            
            self.s_write("!e\r")
            #self.s_read(100)
            print ("Try to get all serial data")
            while (len(self.serial_sigs)<self.number_of_sigs):
                self.s_write("!e\r")
                self.get_serial_data()
                time.sleep(1)
                
            print ("Got all serial data")
            self.old_s_sigs=self.serial_sigs.copy()

        #except:
         #   print ("well the first part didn't work")
        #try:
            self.update_mapper_signals()
            self.poll(m_inst)   
        except:
            print ("Funginble Node initialization failed!")
            raise
            self.close_nicely()
            

        
    
    def close_connection(self):
        try:
            self.s_write("!d\r")
            #self.ser.writelines("!d\r")
            self.ser.close()
        except:
            print ("Could not close port: ", self.port_num)
    
    def s_write(self,message):
        try:
            self.ser.writelines(message)
        except:
            print ("Could not write to port:", self.port_num)
    
    def s_read(self,num_lines):
        try:
            
            if((self.ser.inWaiting()>0)):
#                print ("num in waiting", self.ser.inWaiting())
               # self.inBuffer=self.ser.readlines(num_lines)
    #            print ("type in waiting: ", type(self.ser.inWaiting()))
                
                self.inBuffer=self.ser.read(int(self.ser.inWaiting()))
                self.inBuffer=self.temp_buff+self.inBuffer
                self.temp_buff=""
                buff_length=len(self.inBuffer)
                d_indx=self.inBuffer.rfind("\n")
                if (d_indx>-1): #there is a carriage return
                    try:
                        self.temp_buff=self.inBuffer[d_indx+1:buff_length-1]
                    except:
                        pass
                    self.inBuffer=self.inBuffer[0:d_indx]
                    self.inBuffer=self.inBuffer.split("\n")
                    
                else: #no carriage return, store partial buffer
                    self.temp_buff=self.inBuffer
                    self.inBuffer=""
         
                return self.inBuffer
            #output_buff=self.ser.readlines(num_lines)
            #return output_buff
            else:
#                print("nothing in serial buffer")
                return ""
        except:
            print ("Could not read from port:", self.port_num)
            raise
            return ""
        

#    def close_thread(self):
 #           self.p.join()
    
    def close_nicely(self):
        self.quit=1
        self.close_connection()
#        self.close_thread()
            
    
    def open_connection(self):
#        print self.port_num
 #       print self.baud
        try:
            self.ser = serial.Serial(self.port_num,self.baud,timeout=1)
            #print self.ser
        except:
            print ("Could not open port: " , self.port_num)

    def get_i2c_address(self):
            self.s_write("!d\r")
            #self.ser.writelines("!d\r")
            self.ser.flushInput()
            time.sleep(1)
            self.s_write("SI 0\r")
            #self.ser.writelines("SI 0\r")
            #s = self.ser.readlines(20)
            s = self.s_read(200)
            #print ("printing s, line 176", s)
            try:
                if len(s)>1:

                        for word in s:
                            
                                if ("I2C Slave Address:" in word):
                                        address = word.split("I2C Slave Address:")
                                        self.addr=int(address[1])
                                        return self.addr
            except:                        
                self.addr=0
                print ("I2C address not found")
                return self.addr
    
    def get_signal_info(self):
            
            self.s_write("!d\r")
           
            self.s_write("Sc 5\r")
            time.sleep(1)
            self.s_write("SSR\r")

            time.sleep(1)
            self.ser.flushInput()
            self.s_write("Sbc\r")
            
            
            time.sleep(1)
            #self.ser.writelines("!d\r")
            #self.ser.writelines("Sbb\r")
          #  print "************Reading Serial Content after Sbb***********"
          #  s = self.s_read(60)
            s = self.s_read(200)
            #s = self.ser.readlines(100)
            print "number of lines:"
            print (len(s))
            print "content"
            print (s)
         
  #          self.pairs={}
            item_num=0
 #           self.sig_names={}
#            self.info_index={}
            if len(s)>1:
                for word in s:
#                    length_position = 
                    if (word.find("Length of List of Printed signals:") != -1):
                       # print ("word at 214" ,word)
                       # index_colon = word.find(":")
                        #num_sig = word[index_colon+1:len(word)]
                        num_sig=word.split('Length of List of Printed signals:')
#                        if(num_sig[1].isdigit()):
                        self.number_of_sigs = int(num_sig[1])
                        print "Number of Signals:", self.number_of_sigs
                            
                    elif (word.find("List of Printed signals:")!=-1):
                        #print ("word at 219 " ,word)
                        substr=word.split(':')
                        #print ("substr " ,substr)
                        lnames=substr[1].split()
                        print ("lnames " ,lnames)
                        for item in lnames:
                            sub_item=item.split()
                            self.pairs[item_num]=sub_item[0]
                            item_num=item_num+1
                        item_num=0
                        for item_num in self.pairs.keys():
                            list_num=0
                            for element in sensorinfo:
                                if ((self.pairs[item_num] in element[1]) & (self.addr == element[0])):
                                    #print (item_num,"index gives",element[2] ,element[3], element[4])
                                    self.sig_names[item_num]=str(element[0]) +'/'+ element[2] + '/' + element[3] +'/'+ element[4]
                                    # allboards creates the mapper signal name and is also used to index information from sensorinfo
                                    self.info_index[item_num]=list_num
                                    #info_index directly gives the corresponding row number (i.e. index) of the (board_number, signal_number) pair from sensorinfo
                                    #without having to refer through the 0S1, 1S1, 2S1, etc. notation
                                list_num=list_num+1
#                        print("sig_names",self.sig_names)


    def update_mapper_signals(self):
            
        #for sig_num in range(number_of_mapped_sigs):
        #map_num=0
        #print("signal value ",self.serial_sigs)
        #print ("for board ", self.port_num)
#        print ("mapper sigs",self.mapper_sigs)
        for sig_num in range(self.number_of_sigs):
            #print("sig number:",sig_num, " value:", self.serial_sigs[sig_num])
            #print("old sig number:",sig_num, " value:", self.old_s_sigs[sig_num])
            #print ("what sigs: ",sig_num)
            if (self.serial_sigs[sig_num] == self.old_s_sigs[sig_num]):
                #Only update data if it has a new value...no point sending the old one again
                #print("signal is the same as before: ", sig_num)
#                print ("not new updating signal: ", sig_num, "val: ", self.serial_sigs[sig_num])
                continue
            else:
                #print ("what sigs: ",self.number_of_sigs)
#                print ("updating signal: ", sig_num, "val: ", self.serial_sigs[sig_num])
                

                self.mapper_sigs[sig_num].update(self.serial_sigs[sig_num])
                #print("sig number:",sig_num, " value:", self.serial_sigs[sig_num])
                #print("old sig number:",sig_num, " value:", self.old_s_sigs[sig_num])
        
           # map_num=map_num+1


    def create_mapper_signals(self,m_inst):
#        print ("sig names.keys", self.sig_names.keys())
#        print ("info index", self.info_index)
        for sig in self.sig_names.keys():
            #for sig in allboards[board].keys():
            if  (sensorinfo[self.info_index[sig]][1][1]=='D'):
                max_size=255
            elif (sensorinfo[self.info_index[sig]][1][1]=='S'):
                max_size=128

#            print "max size", max_size
            self.mapper_sigs[sig] = m_inst.add_output(self.sig_names[sig],'i',"Volts",0,max_size)

            print "Created Mapper Signals", self.sig_names[sig] 
    
    def get_serial_data(self):
            
        machine = { (0, 8): 1,
                    (1, 8): 2,
                    (2, 8): 3,
                    (3, 8): 4,
                    (4, 0): 0}

        lines=self.s_read(50)
        #lines=self.ser.readlines(6)
        #print ("length of serial buff: ", len(lines))
        #print ("lines at 358: ", lines)
        self.old_s_sigs=self.serial_sigs.copy()
        for s in lines:
            data = s.split()
            #print "Data Coming In", data                
            L = len(data)

            try:
                self.state = machine[(self.state, L)]
            except:
                self.state = 0
            
            #print ('data', data, 'state', self.state)

            for i in range(8):
                if self.state==1 and L==8:
                    try:
                        #print ("getting signalin state 1")
                        self.serial_sigs[i]=int(data[i])
                        #print ("sigs 2", self.serial_sigs[i])
                    except:
                        print ("Signal is beyond range (not evenly divisible by 8)")
                    #mapper_signals[active_board][i].update(int(data[i]))
                    #print "Active Signal Being Updates", mapper_signals[active_board][i]
                    #print "Data given to active board", data[i]
                    
                if self.state==2 and L==8:
                    try: 
                        #print ("getting signalin state 2")
                        self.serial_sigs[i+8]=int(data[i])
                       # print ("sigs 2", self.serial_sigs[i+8])
                    except:
                        print ("Signal is beyond range (not evenly divisible by 8)")
                   # mapper_signals[active_board][i+8].update(int(data[i]))
                        #print "Active Signal Being Updates", mapper_signals[active_board][i]
                        #print "Data given to active board", data[i]
                
                if self.state==3 and L==8:
                    try: 
                        self.serial_sigs[i+16]=int(data[i])
                    except:
                        print ("Signal is beyond range (not evenly divisible by 8)")
                   # mapper_signals[active_board][i+16].update(int(data[i]))
        
                if self.state==4 and L==8:
                    try: 
                        self.serial_sigs[i+24]=int(data[i])
                    except:
                        print ("Signal is beyond range (not evenly divisible by 8)")
                   # mapper_signals[active_board][i+24].update(int(data[i]))
                
        #return state       

    def f(self,q):
#    def f(q):
            import Tkinter
            def tcall():
                    temp_str=tbox.get()
                    q.put(temp_str)
                    
            def onquit():
                    q.put("quit")
                    root.quit()

            def ontimer():
                    print 'someshit'
  #                  check the serial port
                    root.after(5, ontimer)

            root = Tkinter.Tk()

            quit_button = Tkinter.Button(root, text="Quit", command=lambda: onquit())
            quit_button.pack()

            #command_button = Tkinter.Button(root, text="Enter command for port: "+self.port_num,  command=tcall)
            command_button = Tkinter.Button(root, text="Enter command for port:", command=tcall)
            command_button.pack()

            tbox=Tkinter.Entry(root)
            tbox.pack()
            root.after(5, ontimer)
    #        root.mainloop()

    
    def poll(self,m_inst):
        m_inst.poll(0)
