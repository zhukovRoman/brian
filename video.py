from brian2 import *
from matplotlib import rc
import matplotlib.pyplot as plt
import png
import helpers as helpers

prefs.codegen.target = 'numpy'


# setup
width = 320 
height = 240
neuron_inputs_count = width * height 
tau = 10*ms
eqs = '''
dv/dt = (v0 - v) / tau : volt (unless refractory)
v0 : volt
row : integer (constant)
column : integer (constant)
'''


frame_count = 120
time_between_frames = 4.0*second/frame_count
###############

frames = [0] * frame_count
for picture_number in range(frame_count):
	print('load picture #' + str(picture_number+1))

	f = open('films/two_mans/input_'+str(picture_number+1)+'.png', 'rb')      # binary mode is important
	#f = open('films/horses/input_'+str(picture_number+1)+'.png', 'rb')      # binary mode is important
	r=png.Reader(f)
	pngdata = list(r.read()[2])
	image_2d = []
	for row_number in range(len(pngdata)):
		row = pngdata[row_number]
		image_2d.append(row)
	frames[picture_number] = image_2d
	f.close()


current_frame_index = -1

@check_units(columns_index=1, row_index=1, result=1)
def video_input(columns_index, row_index):

	global current_frame_index 
	current_frame_index = current_frame_index + 1 
	if current_frame_index == frame_count:
		current_frame_index = 0
	result = []
	currentImage = frames[current_frame_index]
	#print('aaaa' , columns_index, row_index )
	for neuron_index in range(len(columns_index)):
		# print('neurin index = ',neuron_index)
		result.append((255-currentImage[columns_index[neuron_index]][row_index[neuron_index]])/(255/24))
	# print('result = ', result)	
	return result


inputNeurons = NeuronGroup(neuron_inputs_count, eqs, threshold='v >= 19*mV', reset='v = 0*mV',
                    refractory=10*ms, method='linear')
inputNeurons.v = 0*mV
inputNeurons.row = 'i/width'
inputNeurons.column = 'i%width'
# group.v0 = '20*mV * 1'

inputNeurons.run_regularly('''v0 = video_input(row, column)*mV''',
                dt=time_between_frames)


mon = SpikeMonitor(inputNeurons)
run(4.0*second, report='text')

# spike_trains = mon.spike_trains(); 

# print(spike_trains)


font = {'family': 'PTSans',
        'weight': 'normal',
        'size': 14}
plt.figure(figsize=(13, 5))
plot(mon.t/ms, mon.i, '.k')
xlabel(u"Время (мс)", family="verdana")
ylabel(u"Номер нейрона", family="verdana")
# savefig('Image_example_cat'+'.png');
savefig('video_example_mans'+'.png');

