"""The backend that operate YOKOGAWA.

"""
import pyvisa
rm = pyvisa.ResourceManager()
connected_insts = {} # the addr -> pyvisa.resource map

def connect(address) -> str:
    """Connect to YOKOGAWA, check if output is on.
    
    raise:

    """
    # # try connecting, using pyvisa
    # try:
    #     inst = rm.open_resource(address)
    # except pyvisa.VisaIOError as e:
    #     raise Exception(f'Error occur when try connecting to YOKOGAWA with addr "{address}".\n{e}')
    
    # # check if the output is on
    # output_status = inst.query(':OUTP?')
    # if output_status == '1\n':
    #     inst.close()
    #     raise Exception(f'The YOKOGAWA with addr "{address}" is outpting, connection halt.')
    
    # # connection success
    # connected_insts[address] = inst
    # print(f'Have connected to YOKOGAWA with addr "{address}".')
    return True

        
def disconnect(address):
    """
    """
    # check if in charge
    if address not in connected_insts.keys():    
        raise Exception(f'There was no YOKOGAWA with addr "{address}" in connection by this artitecture.')
    inst = connected_insts[address]
    
    # check if output is off
    output_status = inst.query(':OUTP?')
    if output_status == '1\n':    
        raise Exception(f'The YOKOGAWA with addr "{address}" is outpting, disconnection halt.')

    # turn the remote light off and delete pyvisa control, remove from dict.
    inst.write(':SYST:LOC')
    inst.close()
    del connected_insts[address]
    print(f'YOKOGAWA with addr {address} is now disconnected.')
    return True

import time
def operate(address, v_max, rising_time, flat_time, pm):
    """Operate the swtich based on the parms
    
    Args:
        address (string): the YOKOGAWA address
        v_max (float): the maxima voltage in volt.
        rising_time (float): the linear rising and falling time from 0 to max.
        flat_time (float): the time voltage steys at maxima vaule.
        pm (str): '+' or '-', voltage goes to +v_max and -v_max respectively.

    Returns:
        complete (bool): ture when success.
    """
    # if address not in connected_insts.keys():    
    #     raise Exception(f'There was no YOKOGAWA with addr "{address}" in connection by this artitecture.')
    # inst = connected_insts[address]
    # ## 
    # # the implimentation
    # ##
    
    # print(f"Operate with {address}, {v_max}, {rising_time}, {flat_time}, {pm}")
    time.sleep(2*rising_time+flat_time)
    return True
