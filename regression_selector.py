import numpy as np
import math
import scipy.integrate as integrate

# As per the implementation in MAML, generate random amplitude-phase pairs
# Only output those pairs that create sufficiently different sinusoids
def sinusoid_selector(batch_size, amp_range, phase_range, input_range):
    epsilon = 4*amp_range[1]
    func_count = 0
    out_amp = np.zeros([batch_size])
    out_phase = np.zeros([batch_size])
    while func_count < batch_size:
        test_amp = np.random.uniform(amp_range[0], amp_range[1], [batch_size])
        test_phase = np.random.uniform(phase_range[0], phase_range[1], [batch_size])
        i = 0
        for func in range(batch_size):
            unique = True
            for i in range(func_count):
                if function_distance(test_amp[func], test_phase[func], out_amp[i], out_phase[i], input_range) < epsilon:
                    unique = False
            if unique:
                out_amp[func_count] = test_amp[func]
                out_phase[func_count] = test_phase[func]
                func_count += 1
                if func_count == batch_size:
                    break
        epsilon *= 0.9**func_count
    return [out_amp, out_phase]
    
# Calculate the distance between functions according to the L^2 Norm
def function_distance(amp1, phase1, amp2, phase2, input_range):
    return math.sqrt(integrate.quad(lambda x: (amp1*np.sin(x-phase1) - amp2*np.sin(x-phase2))**2, input_range[0], input_range[1])[0])