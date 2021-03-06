from brian2 import *
import matplotlib.pyplot as plt
import png
import helpers as helpers

prefs.codegen.target = 'numpy'

n = 10
tau = 10*ms
eqs = '''
dv/dt = (v0 - v) / tau : volt (unless refractory)
v0 : volt
row : integer (constant)
column : integer (constant)
'''


inputVector = [1,2,3,4,5,6,7,8,9,10]
@check_units(columns_index=1, row_index=1, result=1)
def video_input(columns_index, row_index):
	
	result = []
	for neuron_index in range(len(columns_index)):
		result.append(inputVector[neuron_index]*20000)
	print ('return  = ', result)		
	return result

inputNeurons = NeuronGroup(n, eqs, threshold='v >= 100*mV', reset='v = 0*mV',
                    refractory=5*ms, method='linear')
inputNeurons.v = 0*mV
# group.v0 = '20*mV * 1'

inputNeurons.run_regularly('''v0 = video_input(row, column)*mV''',
                dt=0.05*second)


mon = SpikeMonitor(inputNeurons)
run(0.5*second, report='text')

spike_trains = mon.spike_trains(); 

print(spike_trains)

plt.figure(figsize=(10, 5))
plot(mon.t/ms, mon.i+1, '.k')
margins(0.05)
yticks(arange(1, 11, 1))
xlabel(u"Время (мс)", family="verdana")
ylabel(u"Номер нейрона", family="verdana")
savefig('Vecrtor_example'+'.png');