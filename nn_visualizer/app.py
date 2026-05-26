import tkinter as tk
import random
import numpy as np
from math import *
import time
root=tk.Tk()
root.geometry("1200x700")
slider_frame=tk.Frame(root)
slider_frame.pack(pady=10)   
canvas=tk.Canvas(root,bg="#dfe6e9",height=600,width=1200)
layers=[3,4,2]
r=30
entry=tk.Entry(root)
entry.pack()
def set_layers():
    global layers
    text=entry.get()
    layers=[int(x) for x in text.split(',')]
    create_slider()
    generate_network()
    generate_weights()
    generate_bias()
    forward_propagation()
    canvas.delete("all")
    draw_network()
button=tk.Button(root,text="Set Layers",command=set_layers)
button.pack()

def draw_neuron(x,y,radius,color,activation):
    canvas.create_oval(x-radius,y-radius,x+radius,y+radius,fill=color)
    canvas.create_text(x,y,text=f"{activation:.2f}")
def connect_neuron(x1,y1,x2,y2,thickness,color):
    canvas.create_line(x1,y1,x2,y2,fill=color,width=thickness)
def generate_network():
    
    global layers
    global r
    global final_list
    final_list=[]
    for layer_index in range(len(layers)):
        neuron_count=layers[layer_index]
        layer_position=[]
        neurons=layers[layer_index]
        #total_height=spacing*(neurons-1)
        #start_y=center-total_height//2
        #x=x_positions[layer_index]
        for neuron_index in range(neuron_count):
            x=200 +layer_index*250
            y=300 + (neuron_index-neuron_count/2)*100
            activation=0
            #draw_neuron(x,y,r,color)
            layer_position.append((x,y,0))
        final_list.append(layer_position)
def draw_network():
    global final_list
    for layer_index in range(len(final_list)-1):
        current_layer=final_list[layer_index]
        next_layer=final_list[layer_index+1]
        for current_index,neuron1 in enumerate(current_layer):
            x,y,_=neuron1
            for next_index,neuron2 in enumerate(next_layer):
                x1,y1,th=neuron2
                weight=all_weights[layer_index][next_index][current_index]
                thickness=abs(weight)*5
                if weight>0:
                    color="green"
                else:
                    color="red"
                connect_neuron(x,y,x1,y1,thickness,color)
        
    for i in final_list:
        for j in i:
            x,y,act=j
            brightness=int(abs(act)*255)
            color=f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            draw_neuron(x,y,r,color,act)
            layer_index=final_list.index(i)
            neuron_index=i.index(j)
            if layer_index!=0:
                bias=all_biases[layer_index-1][neuron_index]
                canvas.create_text(x,y+40,text=f"b:{bias:.2f}",fill="black")
def update_network(value=None):
    global final_list
    input_values=[]
    input_values=[slider.get() for slider in sliders]
    for i in range(len(input_values)):
        x=final_list[0][i][0]
        y=final_list[0][i][1]
        final_list[0][i]=(x,y,input_values[i])
    canvas.delete("all")
    forward_propagation()
    draw_network()
sliders=[]
def create_slider():
    for slider in sliders:
        slider.destroy()
    sliders.clear()
    for i in range(layers[0]):
        mini_frame=tk.Frame(slider_frame,bg="#dfe6e9")
        mini_frame.pack(side="left",padx=20)
        slider=tk.Scale(mini_frame,from_=-1,to=1,resolution=0.01,orient="horizontal",command=update_network)
        slider.pack()
        label=tk.Label(mini_frame,text=f"Input{i}",bg="#dfe6e9")
        label.pack()
        sliders.append(slider)
def sigmoid(x):
    return 1/(1+exp(-x))
def relu(x):
    return max(0,x)
def tanh_activation(x):
    return tanh(x)
activation_function=sigmoid
def generate_weights():
    global all_weights
    all_weights=[]
    for layer_index in range(len(layers)-1):
        current_layer_size=layers[layer_index]
        next_layer_size=layers[layer_index+1]
        layer_weights=[]
        for next_neuron in range(next_layer_size):
            neuron_weights=[]
            for current_neuron in range(current_layer_size):
                neuron_weights.append(random.uniform(-1,1))
            layer_weights.append(neuron_weights)
        all_weights.append(layer_weights)

def use_relu():
    global activation_function
    activation_function=relu
    update_network()
def use_sigmoid():
    global activation_function
    activation_function=sigmoid
    update_network()
def use_tanh():
    global activation_function
    activation_function=tanh_activation
    update_network()

def forward_propagation(animated=False):
    global final_list
    '''weight_value=[]
    for i in range(len(input_values)):
        x=final_list[0][i][0]
        y=final_list[0][i][1]
        final_list[0][i]=(x,y,input_values[i])

    for i in range(layers[1]):
        weights=[]
        for j in range(layers[0]):
            weights.append(random.uniform(-1,1))
        weight_value.append(weights)
    z_value=[]
    for i in weight_value:
        z=np.dot(input_values,np.array(i))
        z_value.append(z)
    for i in range(len(z_value)):
        x=final_list[1][i][0]
        y=final_list[1][i][1]
        final_list[1][i]=(x,y,z_value[i])

    output_weights=[]
    for i in range(layers[-1]):
        output=[]
        for j in range(len(z_value)):
            output.append(random.uniform(-1,1))
        output_weights.append(output)
    z_out_value=[]
    for i in output_weights:
        z=np.dot(z_value,np.array(i))
        z_out_value.append(z)
    for i in range(len(output_weights)):
        x=final_list[-1][i][0]
        y=final_list[-1][i][1]
        final_list[-1][i]=(x,y,z_out_value[i])'''
    for layer_index in range(len(final_list)-1):
        current_layer=final_list[layer_index]
        next_layer=final_list[layer_index+1]
        for next_neuron in range(len(next_layer)):
            z=all_biases[layer_index][next_neuron]
            for current_neuron in range(len(current_layer)):
                current_activation=current_layer[current_neuron][2]
                weight=all_weights[layer_index][next_neuron][current_neuron]
                z+=current_activation*weight
            activation=activation_function(z)
            x=next_layer[next_neuron][0]
            y=next_layer[next_neuron][1]
            final_list[layer_index+1][next_neuron]=(x,y,activation)         
    if animated:
        canvas.delete("all")
        draw_network()
        root.update()
        time.sleep(0.3)
def generate_bias():
    global all_biases
    all_biases=[]
    for layer_index in range(1,len(layers)):
        
        layer_biases=[]
        for neuron in range(layers[layer_index]):
            layer_biases.append(random.uniform(-1,1))
        all_biases.append(layer_biases)
sigmoid_button=tk.Button(root,text="sigmoid",command=use_sigmoid)
sigmoid_button.pack()
relu_button=tk.Button(root,text="reLU",command=use_relu)
relu_button.pack()
tanh_button=tk.Button(root,text="tanh",command=use_tanh)
tanh_button.pack()
generate_network()
generate_weights()
generate_bias()
forward_propagation()
draw_network()
canvas.pack()
root.mainloop()
