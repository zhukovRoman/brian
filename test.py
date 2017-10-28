

from brian2 import *
import matplotlib.pyplot as plt

start_scope()

# generate inputs
def generateInputs(pixels):
	generators = []
	for pixel in pixels:
		generators.append(PoissonGroup(1, pixel*Hz))
	return generators	


# indices = array([0, 1, 1, 1, 0])
# times = array([1, 2, 3, 4, 5])*ms
# G = SpikeGeneratorGroup(3, indices, times)
pixels = [10, 255, 10, 255]
generators = generateInputs(pixels)



# for p in generators: print(p)

# print ('---------')

gen1 = generators[0]
monitor1 = SpikeMonitor(gen1)
gen2 = generators[1]
monitor2 = SpikeMonitor(gen2)
gen3 = generators[2]
monitor3 = SpikeMonitor(gen3)
gen4 = generators[3]
monitor4 = SpikeMonitor(gen4)

monitors = []
indexes = []
i = 0;
for gen in generators:
	print(gen)
	monitors.append(SpikeMonitor(generators[i]))
	i+=1

# # G = NeuronGroup(4, 'dv/dt = -v / (10*ms) : 1')

for p in monitors: print(p)

run(1000*ms)

# v_values = monitor1.values('t')
# print('Threshold crossing values for mon1: {}'.format(v_values[0]))
# v_values = monitor2.values('t')
# print('Threshold crossing values for mon2: {}'.format(v_values[0]))
# v_values = monitor3.values('t')
# print('Threshold crossing values for mon3: {}'.format(v_values[0]))
# v_values = monitor4.values('t')
# print('Threshold crossing values for mon4: {}'.format(v_values[0]))

# i = 0
for mon in monitors:
	print(mon)
	v_values = mon.values('t')
	print('Threshold crossing values for neuron : {}'.format(v_values[0]))
	# plot(mon.t/ms, mon.i, '.k')
	# xlabel('Time (ms)')
	# ylabel('Neuron index')
	# savefig('spikeGenerator'+str(i)+'.png');
	# i += 1
	
