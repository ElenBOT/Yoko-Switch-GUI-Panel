"""The backend that operate YOKOGAWA.

"""
import pyvisa
import time
rm = pyvisa.ResourceManager()
connected_insts = {} # the addr -> pyvisa.resource map

def connect(address: str) -> bool:
    """Connect to YOKOGAWA, check if output is on.
    
    Raises:
        pyvisa.VisaIOError: If the connection to the instrument cannot be established
            (e.g., invalid address, communication error).
        Exception: If the instrument output is already ON, the connection is
            aborted for safety reasons.
    """
    # try connecting, using pyvisa
    yoko = rm.open_resource(address) # raise: pyvisa.VisaIOError
    
    # check if the output is on
    output_status = yoko.query(':OUTP?')
    if output_status == '1\n':
        yoko.close()
        raise Exception(f'The YOKOGAWA with addr "{address}" is outpting, connection halt.')
    
    # connection success
    connected_insts[address] = yoko
    print(f'Have connected to YOKOGAWA with addr "{address}".')
    return True

        
def disconnect(address: str) -> bool:
    """
    
    Raises:
        Exception: If the instrument with the given address is not currently
            managed by this backend (not connected).
        Exception: If the instrument output is still ON, the disconnection is
            halted for safety reasons.
    """
    # check if in charge
    if address not in connected_insts.keys():    
        raise Exception(f'There was no YOKOGAWA with addr "{address}" in connection by this artitecture.')
    yoko = connected_insts[address]
    
    # check if output is off
    output_status = yoko.query(':OUTP?')
    if output_status == '1\n':    
        raise Exception(f'The YOKOGAWA with addr "{address}" is outpting, disconnection halt.')

    # turn the remote light off and delete pyvisa control, remove from dict.
    yoko.write(':SYST:LOC')
    yoko.close()
    del connected_insts[address]
    print(f'YOKOGAWA with addr {address} is now disconnected.')
    return True

_double_click_blocking_addr = []
def operate(address, v_max, rising_time, flat_time, pm):
    """Operate the swtich based on the parms.
    
    Args:
        address (string): the YOKOGAWA address
        v_max (float): the maxima voltage in volt.
        rising_time (float): the linear rising and falling time from 0 to max.
        flat_time (float): the time voltage steys at maxima vaule.
        pm (str): '+' or '-', voltage goes to +v_max and -v_max respectively.

    Raises:
        KeyError: If the instrument is not in charge.
        ValueError: If the pm option, rising_time, flat_time, v_max is invalid.
        Exception: If the YOKOGAWA outpiting when calling this function.
        
    Returns:
        complete (bool): ture when success.
    """
    if address in _double_click_blocking_addr:
        return False
    if address not in connected_insts.keys():    
        raise KeyError(f'There was no YOKOGAWA with addr "{address}" in connection by this artitecture.')
    yoko = connected_insts[address]
    output_status = yoko.query(':OUTP?')
    if output_status == '1\n':    
        raise Exception(f'The YOKOGAWA with addr "{address}" is outpting, halt.')
    
    ## init
    _double_click_blocking_addr.append(address)
    yoko.write('*CLS')
    yoko.write(':PROG:REP 0')
    yoko.write(':SOUR:LEV 0')
    yoko.write(':SOUR:FUNC VOLT')
    
    ## config
    if rising_time < 0 or rising_time > 3600:
        raise ValueError(f'The rising time {rising_time} is invalid (should be 0 ~ 3600s).')
    if flat_time < 0:
        raise ValueError(f'The flat time {flat_time} is invalid (should be > 0).')
    if v_max <= 0:
        raise ValueError(f'The v_max {flat_time} is invalid (should be > 0).')
    if pm != '+' and pm != '-':
        raise ValueError(f'The pm option {pm} is not "+" nor "-".')
    # set voltage range to sutiable
    volt_ranges = [1e-3, 1e-2, 1e-1, 1, 10, 30] # VOLT range
    for volt_range in volt_ranges:
        if v_max <= volt_range:
            yoko.write(f":SOUR:RANG {volt_range}")
            break
    else:
        raise ValueError(f"v_max {v_max}V is out of range {volt_range}V")
    yoko.write(f':PROG:SLOP {rising_time:.6e}') # rising time
    yoko.write(f':PROG:INT {rising_time:.6e}')  # program time interval

    yoko.write(':OUTP ON')
    ## rising
    if pm == '+': flat_level = v_max
    elif pm == '-': flat_level = -v_max
    yoko.write(':PROG:EDIT:STAR;')
    yoko.write(f':SOUR:LEV {flat_level}')
    yoko.write(':PROG:EDIT:END;')
    yoko.write(':PROG:RUN')
    time.sleep(rising_time)

    ## flat
    time.sleep(flat_time)
    
    ## falling
    yoko.write(':PROG:EDIT:STAR;')
    yoko.write(':SOUR:LEV 0')
    yoko.write(':PROG:EDIT:END;')
    yoko.write(':PROG:RUN')
    time.sleep(rising_time*1.1)

    ## ending
    yoko.write(':OUTP OFF')
    _double_click_blocking_addr.remove(address)

    return True

