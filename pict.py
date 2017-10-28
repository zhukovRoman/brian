from brian2 import *
import matplotlib.pyplot as plt
import png
import helpers as helpers

prefs.codegen.target = 'numpy'

# setup 
width, height = 15, 15
neuron_inputs_count = width * height

frame_count = 38
time_between_frames = 1.0*second/frame_count
###############


frames = [0] * frame_count
for picture_number in range(frame_count):
	print('load picture #' + str(picture_number+1))

	f = open('images/'+str(picture_number+1)+'.png', 'rb')      # binary mode is important
	r=png.Reader(f)
	pngdata = list(r.read()[2])
	image_2d = []
	for row_number in range(len(pngdata)):
		row = pngdata[row_number]
		image_2d.append(row)
	frames[picture_number] = image_2d
	f.close()

#print(inputs_pict[1][1][0], inputs_pict[1][1][1], inputs_pict[1][1][2], inputs_pict[1][1][3]) 

current_frame_index = -1

@check_units(columns_index=1, row_index=1, result=1)
def video_input(columns_index, row_index):
	global current_frame_index 
	current_frame_index = current_frame_index + 1 
	if current_frame_index == frame_count:
		current_frame_index = 0
	# print ('geting pixels from frame = ', current_frame_index)	
	
	result = []
	for neuron_index in range(len(columns_index)):
		result.append(255-frames[current_frame_index][row_index[neuron_index]][columns_index[neuron_index]])
	return result

tau, tau_th = 10*ms, 10*ms
inputNeurons = NeuronGroup(neuron_inputs_count, '''dv/dt = (-v + I)/tau : 1
                      dv_th/dt = -v_th/tau_th : 1
                      row : integer (constant)
                      column : integer (constant)
                      I : 1 # input current''',
                threshold='v>v_th', 
                reset='v=0; v_th = 3*v_th + 1.0',
                method='linear')

inputNeurons.v_th = 1
inputNeurons.row = 'i/width'
inputNeurons.column = 'i%width'

inputNeurons.run_regularly('''I = video_input(row, column)''',
                dt=time_between_frames/2)

recognitionNeurons = NeuronGroup(neuron_inputs_count, 
								'''dv/dt = (-v + I)/tau : 1
				                      dv_th/dt = -v_th/tau_th : 1
				                      row : integer (constant)
				                      column : integer (constant)
				                      I : 1 # input current''',
				                threshold='v>v_th', 
				                reset='v=0; v_th = 3*v_th + 1.0',
								refractory=100*ms, method='linear')
recognitionNeurons.v_th = 1
recognitionNeurons.row = 'i/width'
recognitionNeurons.column = 'i%width'

taupre = taupost = 200*ms
wmax = 1
Apre = 0.1
Apost = -Apre*taupre/taupost*1.05

S = Synapses(inputNeurons, recognitionNeurons, '''
	             w : 1
	             dapre/dt = -apre/taupre : 1 (clock-driven)
	             dapost/dt = -apost/taupost : 1 (clock-driven)
             ''',
             on_pre='''
	             v_post += w
	             apre += Apre
	             w = clip(w+apost*2, 0, wmax)
             ''',
             on_post='''
	             apost += Apost
	             w = clip(w+apre*2, 0, wmax)
             ''')

S.connect(condition='abs(i-j)<4', p=0.5)
# S.w = 'exp(-(row_pre-row_post)**2/(1*1**2))'
S.w = '0.5'
# helpers.visualise_connectivity(S)

mon = SpikeMonitor(inputNeurons)
mon2 = SpikeMonitor(recognitionNeurons)
runtime = frame_count*time_between_frames*20
run(runtime, report='text')

plt.figure(figsize=(10, 4))
plot(mon.t/ms, mon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
savefig('spikeGenerator'+'.png');

plt.figure(figsize=(10, 4))
plot(mon2.t/ms, mon2.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
savefig('spikeGenerator2'+'.png');
