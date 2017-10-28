from brian2 import *
from matplotlib import rc
import matplotlib.pyplot as plt
import png
import helpers as helpers

prefs.codegen.target = 'numpy'


# setup
width = 3
height = 1
neuron_inputs_count = width * height 
tau = 150*ms
eqs = '''
dv/dt = (v0 - v) / tau : volt (unless refractory)
v0 : volt
row : integer (constant)
column : integer (constant)
'''

###############

activities = ['walking', 'walking_up', 'walking_down', 'all']
currentActivity = activities[2]
values1 = []
values2 = []
values3 = []



with open('diods/'+ currentActivity +'/diod1.txt') as f:
    content = f.readlines()
    values1 = [float(x.strip()) for x in content] 
#print(values1)    

with open('diods/'+ currentActivity +'/diod2.txt') as f:
    content = f.readlines()
    values2 = [float(x.strip()) for x in content] 

# with open('diods/'+ currentActivity +'/delta.txt') as f:
#     for x in f.readline().strip().split():
#     	values3.append(float(x))

current_frame_index = -1
print(len(values2), len(values1))

@check_units(columns_index=1, row_index=1, result=1)
def video_input(columns_index, row_index):

	global current_frame_index 
	current_frame_index = current_frame_index + 1 
	if current_frame_index == frame_count:
		current_frame_index = 0
	result = []
	#print('result = ', [acc_x[current_frame_index], acc_y[current_frame_index], acc_z[current_frame_index], g_x[current_frame_index], g_y[current_frame_index], g_z[current_frame_index]])	
	return [values1[current_frame_index], values2[current_frame_index]*1, values1[current_frame_index]-values2[current_frame_index]]

frame_count = len(values1)
time_between_frames = 1*second/100

inputNeurons = NeuronGroup(neuron_inputs_count, eqs, threshold='v >= 100*mV', reset='v = 0*mV',
                    refractory=10*ms, method='linear')
inputNeurons.v = 0*mV
inputNeurons.row = '0'
inputNeurons.column = 'i%width'
# group.v0 = '20*mV * 1'

inputNeurons.run_regularly('''v0 = video_input(row, column)*5*mV''',
                dt=time_between_frames)


mon = SpikeMonitor(inputNeurons)
run(frame_count*time_between_frames, report='text')

# # spike_trains = mon.spike_trains(); 

# # print(spike_trains)


font = {'family': 'PTSans',
        'weight': 'normal',
        'size': 20}
plt.figure(figsize=(20, 5))
plot(mon.t/ms, mon.i+1, '.k')
margins(0.05)
yticks(arange(1, 4, 1))
xlabel(u"Время (мс)", family="verdana")
ylabel(u"Номер нейрона", family="verdana")
# savefig('Image_example_cat'+'.png');
savefig('donsee_'+ currentActivity +'.svg', format="svg");

