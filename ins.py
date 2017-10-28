from brian2 import *
from matplotlib import rc
import matplotlib.pyplot as plt
import png
import helpers as helpers

prefs.codegen.target = 'numpy'


# setup
width = 6
height = 1
neuron_inputs_count = width * height 
tau = 10*ms
eqs = '''
dv/dt = (v0 - v) / tau : volt (unless refractory)
v0 : volt
row : integer (constant)
column : integer (constant)
'''


frame_count = 128
time_between_frames = 2.56*second/frame_count
###############

activities = ['standing', 'walking']
currentActivity = activities[1]
acc_x = []
acc_y = []
acc_z = []
g_x = []
g_y = []
g_z = []

with open('ins/'+ currentActivity +'/acc_x.txt') as f:
    for x in f.readline().strip().split():
    	acc_x.append(float(x))

with open('ins/'+ currentActivity +'/acc_y.txt') as f:
    for x in f.readline().strip().split():
    	acc_y.append(float(x))

with open('ins/'+ currentActivity +'/acc_z.txt') as f:
    for x in f.readline().strip().split():
    	acc_z.append(float(x))

with open('ins/'+ currentActivity +'/g_x.txt') as f:
    for x in f.readline().strip().split():
    	g_x.append(float(x))

with open('ins/'+ currentActivity +'/g_y.txt') as f:
    for x in f.readline().strip().split():
    	g_y.append(float(x))

with open('ins/'+ currentActivity +'/g_z.txt') as f:
    for x in f.readline().strip().split():
    	g_z.append(float(x))    	

current_frame_index = -1

@check_units(columns_index=1, row_index=1, result=1)
def video_input(columns_index, row_index):

	global current_frame_index 
	current_frame_index = current_frame_index + 1 
	if current_frame_index == frame_count:
		current_frame_index = 0
	result = []
	#print('result = ', [acc_x[current_frame_index], acc_y[current_frame_index], acc_z[current_frame_index], g_x[current_frame_index], g_y[current_frame_index], g_z[current_frame_index]])	
	return [acc_x[current_frame_index], acc_y[current_frame_index], acc_z[current_frame_index], g_x[current_frame_index], g_y[current_frame_index], g_z[current_frame_index]]


inputNeurons = NeuronGroup(neuron_inputs_count, eqs, threshold='v >= 10*mV', reset='v = 0*mV',
                    refractory=5*ms, method='linear')
inputNeurons.v = 0*mV
inputNeurons.row = '0'
inputNeurons.column = 'i%width'
# group.v0 = '20*mV * 1'

inputNeurons.run_regularly('''v0 = video_input(row, column)*100*mV''',
                dt=time_between_frames)


mon = SpikeMonitor(inputNeurons)
run(2.56*second, report='text')

# # spike_trains = mon.spike_trains(); 

# # print(spike_trains)


font = {'family': 'PTSans',
        'weight': 'normal',
        'size': 14}
plt.figure(figsize=(13, 5))
plot(mon.t/ms, mon.i+1, '.k')
margins(0.05)
yticks(arange(1, 7, 1))
xlabel(u"Время (мс)", family="verdana")
ylabel(u"Номер нейрона", family="verdana")
# savefig('Image_example_cat'+'.png');
savefig('ins_example_'+ currentActivity +'.png');

