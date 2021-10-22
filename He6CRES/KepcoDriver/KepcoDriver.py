#!/usr/bin/env python2
import socket
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

class dsocket(socket):
    def sendMessage(self,message):
        try: 
            self.send(str.encode(message))
        except RuntimeError: 
            raise RuntimeError("Error: Kepco PS not responding")

class KepcoBIT802E():
    
    
    def __init__(self, dsoc_desc=("10.66.192.42",5025)):
        """
        Initialize a Kepco Power Supply controlled via the BIT 802E Digital Interface Card; 
        open a data socket from the client side for communication
        Note that after recieving a command the BIT 802E responds first with the command itself.
        This first response is denoted message_bounce.
        ----------Parameters----------
        dsoc_desc (tuple): A tuple with the first element the IP address
            and the second element the port where data is to be received. 
        """
        
        self.ds = dsocket(AF_INET,SOCK_STREAM) # Note: SOCK_STREAM is default 
        if not dsoc_desc is None:
            try:
                self.ds.connect(dsoc_desc)
            except RuntimeError:
                raise RuntimeError("Error: Unable to connect to server at {0}".format(dsoc_desc))
        
        # I need to think about if this is the right place for this. 
        
        self.ds.sendMessage("*RST\r\n")
   

    def MessageReturn(self, message):
        """
        Returns string representing KEPCO current in Amps
        """
        self.ds.sendMessage("{}\r\n".format(message))                      
        response = self.ds.recv(100) 
        return response

    
    def MessageNoReturn(self, message):
        """
        Returns string representing KEPCO current in Amps
        """
        self.ds.sendMessage("{}\r\n".format(message))                      
        return None
    

#     def setMode_VOLT(self, MaxCurr):
#         """
#         Sets Kepco Mode to VOLT. VOLT Mode means the supply is Voltage controlled;
#         If you set MaxCurr = .1 A then you can setVolt(x) so long as voltage x doesn't create a current 
#         larger than MaxCurr. Note that an x that puts the current near .1 A (MaxCurr) will 
#         cause the output voltage to be less than x. 
#         """
#         self.ds.sendMessage("FUNC:MODE VOLT") 
#         self.ds.sendMessage("VOLT 0;:OUTP ON\r\n") # For some reason you need to send it a volt command first. 
#         self.ds.sendMessage("CURR {}\r\n".format(MaxCurr)) 
#         return None     
    
    
    def setMode_Curr(self, MaxCurr):
        """
        Sets Kepco Mode to Curr. See comments for setMode_VOLT
        """

        self.MessageNoReturn("FUNC:MODE CURR")
        self.MessageNoReturn("CURR 0;:OUTP ON\r\n")
        self.MaxCurr = MaxCurr

        return None  
    
    def setVolt(self, Volt):
        """
        Returns message sent. 
        """
        self.ds.sendMessage("VOLT {};:OUTP ON\r\n".format(Volt)) 
        return None
   

    def setCurr(self, Curr):
        """
        Returns message sent. 
        """
        if abs(Curr)< self.MaxCurr:  
            self.MessageNoReturn("CURR {};:OUTP ON\r\n".format(Curr)) 
        else: 
            print('ERROR: Exceeded Max Current.')
        return None  
    
    
    def getVolt(self):
        """
        Returns string representing KEPCO voltage in Volts
        """
        self.ds.sendMessage("MEAS:VOLT?\r\n")
        response = self.ds.recv(100) 
        return response

    
    def getCurr(self):
        """
        Returns string representing KEPCO current in Amps
        """
        self.ds.sendMessage("MEAS:CURR?\r\n")                       
        response = self.ds.recv(100)
        return response
    
    

   