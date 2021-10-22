from KepcoDriver import KepcoBIT802E 
import time
import threading

# I am using the pynb by the same name to help in developing this. 

def SlewFunction_Curr(T_up,T_down,duration,CurrValUp,CurrValDown, MaxCurr):
    ''' StepFunction turns the power supply up to CurrVal for T_up seconds
    and down to zero for T_down seconds repeatedly until duration (seconds) has elapsed. '''
    
    # Create an instance of the Kepco Driver:
    ps = KepcoBIT802E()
    
    # Set the supply to CURR mode. Set max current to MaxCurr:
    ps.setMode_Curr(MaxCurr) 
    
    # Construct Array with end of cycle time stamps: 
    T_stamps =[]
    
    # Set up a while loop that will last for "duration".  
    i=0
    timeout_start = time.time()
    while time.time() < timeout_start + duration:
        
        ps.setCurr(CurrValUp)
        time.sleep(T_up)
        ps.setCurr(CurrValDown)
        time.sleep(T_down)
        T_stamps.append(time.time()-timeout_start)
        i+= 1
        
    return T_stamps
            

def SlewFunction_Volt(T_up,T_down,duration,VoltVal):
    ''' StepFunction turns the power supply up to CurrVal for T_up seconds
    and down to zero for T_down seconds repeatedly until 'duration' seconds has elapsed '''
    
    # Create an instance of the power supply
    
    ps = KepcoBIT802E()
    ps.setMode_VOLT(1) # Setting the supply to CURR mode. Setting max voltage to 1v. 
    
    # Setting up a while loop that will last for "duration".  
    i=0
    timeout_start = time.time()
    while time.time() < timeout_start + duration:
        i+= 1
        ps.setVolt(VoltVal)
        print(ps.getVolt())
        time.sleep(T_up)
        ps.setVolt(0.00)
        print(ps.getVolt())
        time.sleep(T_down)
        print('cycle {}'.format(i))    
    
    
    
    
    
