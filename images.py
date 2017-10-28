from brian2 import *
from matplotlib import rc
import matplotlib.pyplot as plt
import png
import helpers as helpers

prefs.codegen.target = 'numpy'


# setup
width, height = 100, 100
neuron_inputs_count = width * height 
tau = 10*ms
eqs = '''
dv/dt = (v0 - v) / tau : volt (unless refractory)
v0 : volt
row : integer (constant)
column : integer (constant)
'''


frame_count = 38
time_between_frames = 1.0*second/frame_count
###############

frames = [0] * frame_count

print('load picture cat')
catImage = [];
leaveImage = [];
demo = []
f = open('two_images/cat_input.png', 'rb')      # binary mode is important
r=png.Reader(f)
pngdata = list(r.read()[2])
image_2d = []
for row_number in range(len(pngdata)):
	row = pngdata[row_number]
	image_2d.append(row)
catImage = image_2d
f.close()

print('load picture leaves')
f = open('two_images/leaves_input.png', 'rb')      # binary mode is important
r=png.Reader(f)
pngdata = list(r.read()[2])
image_2d = []
for row_number in range(len(pngdata)):
	row = pngdata[row_number]
	image_2d.append(row)
leaveImage = image_2d
f.close()


currentImage = leaveImage
# print(len(currentImage[0]))
# print(currentImage[20])
@check_units(columns_index=1, row_index=1, result=1)
def video_input(columns_index, row_index):
	result = []
	# print('indexes=',row_index, columns_index)
	for neuron_index in range(len(columns_index)):
		# print('neurin index = ',neuron_index)
		result.append((255-currentImage[row_index[neuron_index]][columns_index[neuron_index]])/(255/27))
	# print('result = ', result)	
	return result


inputNeurons = NeuronGroup(neuron_inputs_count, eqs, threshold='v >= 19*mV', reset='v = 0*mV',
                    refractory=5*ms, method='linear')
inputNeurons.v = 0*mV
inputNeurons.row = 'i%width'
inputNeurons.column = 'i/width'
# group.v0 = '20*mV * 1'

inputNeurons.run_regularly('''v0 = video_input(row, column)*mV''',
                dt=1*second)


mon = SpikeMonitor(inputNeurons)
run(1.0*second, report='text')

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
savefig('Image_example_leave'+'.png');

