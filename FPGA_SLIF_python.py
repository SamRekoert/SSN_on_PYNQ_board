from pynq import Overlay

ov = Overlay('slif_loop.bit')
ov.ip_dict

slif_ip = ov.slif_0
slif_ip.register_map

import timeit 
n = 1

#The following slif function reads and writes to the FPGA every loop. 
#This works but is very slow.
def slif_slow(): 
    slif_ip.register_map.state_in = 1
    slif_ip.register_map.counter_in = 1
    slif_ip.register_map.in_c = 1
    state = 1
    counter = 1
    spike = 0

    for i in range(0, 5000):

        counter = slif_ip.register_map.counter_out_o
        state = slif_ip.register_map.state_out_o
        spike = slif_ip.register_map.spike
        if int(spike) == 1:
            print(i)
        slif_ip.register_map.state_in = int(state)
        slif_ip.register_map.counter_in = int(counter)

result = timeit.timeit(stmt='slif_slow()', globals=globals(), number=n)
print(f"Execution time is {result / n} seconds")
#output: Execution time is 1.5996724780000022 seconds

#The following slif function does the looping on the FPGA.
#This causes problems, because it won't update the states at the end in the HLS code.
import timeit 
n = 1

def slif_fast(): 
    for i in range(0, 1):
        slif_ip.register_map.state_in = 0
        slif_ip.register_map.counter_in = 0 
        slif_ip.register_map.in_c = 1
        slif_ip.register_map.loops = 1000
        
        counter = slif_ip.register_map.counter_out_o
        state = slif_ip.register_map.state_out_o
        spike = slif_ip.register_map.spike
        if int(spike)==1: print(spike)

result = timeit.timeit(stmt='slif_fast()', globals=globals(), number=n)
print(f"Execution time is {result / n} seconds")


#The following two function are the SLIF neuron without FPGA, which currently 
#performs faster than the FPGA version.
def slif_python(state_in, counter_in, in_c, spike):
    match state_in:
        case 0:
            if (1024 == counter_in):
                state_in = 1
                counter_in = 0
            else:
                state_in = state_in + 1
        case 1:
            if (1024 == counter_in):
                spike = 1
                state_in = 2
                counter_in = 0
            elif (1 == in_c):
                counter_in = counter_in + 1
            elif (counter_in != 0):
                counter_in = counter_in - 1
        case 2:
            spike = 0
            state_in = 0
        case _:
            spike = 0
            state_in = 1
            counter_in = 0
    return spike, state_in, counter_in

n = 1

def run_slif_python(): 
    state_in = 1
    counter_in = 1
    in_c = 1
    spike = 0

    for i in range(0, 5000):
        spike, state_in, counter_in = slif_python(state_in, counter_in, in_c, spike)
        #if spike == 1: print(i)
result = timeit.timeit(stmt='slif_python()', globals=globals(), number=n)
print(f"Execution time is {result / n} seconds")
#Output: Execution time is 0.028009291999978814 seconds