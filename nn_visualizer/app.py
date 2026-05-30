import tkinter as tk
import customtkinter as ctk
import random
import numpy as np
from math import *
import time
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root=ctk.CTk()
root.geometry("1400x850")
root.configure(fg_color="#0f172a")
sidebar=ctk.CTkFrame(root,width=250,corner_radius=0,fg_color="#111827")
sidebar.pack(side="left",fill="y")
main_frame=ctk.CTkFrame(root,fg_color="#0f172a")
main_frame.pack(side="right",fill="both",expand=True)
title=ctk.CTkLabel(sidebar,text="Neural Network Visualizer",font=("Segoe UI",22,"bold"))
title.pack(pady=20)
slider_frame=ctk.CTkFrame(sidebar,fg_color="#1e293b")
slider_frame.pack(padx=15,pady=20,fill="x")
canvas_frame=ctk.CTkFrame(main_frame,fg_color="#0f172a")
canvas_frame.pack(side="left",fill="both",expand=True)

output_frame=ctk.CTkFrame(main_frame,width=250,fg_color="#111827")
output_frame.pack(side="right",fill="y",padx=10,pady=10)
output_frame.pack_propagate(False)
canvas=tk.Canvas(canvas_frame,bg="#0f172a",height=600,width=1200,highlightthickness=0)
canvas.pack(fill="both",expand=True,padx=20,pady=20)
layers=[3,4,2]
radius=35
entry=ctk.CTkEntry(sidebar,placeholder_text="Example : 3,4,2",height=40)
entry.pack(pady=20,padx=20,fill="x")
output_title=ctk.CTkLabel(output_frame,text="Outputs",font=("Segoe UI",18,"bold")
)
output_title.pack(pady=15)
output_labels=[]
def create_output_labels():
    global output_labels
    for label in output_labels:
        label.destroy()
    output_labels=[]
    for i in range(layers[-1]):
        lbl=ctk.CTkLabel(output_frame,text=f"Neuron {i+1}: 0.00" ,font=("Segoe UI",14))
        lbl.pack(pady=5)
        output_labels.append(lbl)
def set_layers():
    global layers
    text=entry.get()
    layers=list(map(int,text.split(",")))
    generate_network()
    generate_weights()
    generate_bias()
    create_slider()
    create_output_labels()
    forward_propagation()
    
    canvas.delete("all")
    draw_network()
button=ctk.CTkButton(sidebar,text="Set Layers",command=set_layers,corner_radius=12,height=40,fg_color="#2563eb",hover_color="#1d4ed8",font=("Inter",11))
button.pack(pady=10,padx=20,fill="x")
def draw_neuron(x,y,radius,color,activation):
    canvas.create_oval(x-radius+4,y-radius+4,x+radius+4,y+radius+4,fill="#000000",outline="")
    canvas.create_oval(x-radius,y-radius,x+radius,y+radius,fill=color,outline="#ffffff")
    canvas.create_text(x,y,text=f"{activation:.2f}",font=("Inter",11))
def connect_neuron(x1,y1,x2,y2,thickness,color):
    canvas.create_line(x1,y1,x2,y2,fill=color,width=thickness)
def generate_network(): 
    global layers
    global r
    global final_list
    final_list=[]
    spacing=130
    layer_spacing=280
    for layer_index in range(len(layers)):
        neuron_count=layers[layer_index]
        layer_position=[]
        x=250+layer_index*layer_spacing

        total_height=spacing*(neuron_count-1)
        start_y=350-total_height/2
        #x=x_positions[layer_index]
        for neuron_index in range(neuron_count):
            y=start_y+neuron_index*spacing
            activation=0
            #draw_neuron(x,y,r,color)
            layer_position.append((x,y,activation))
        final_list.append(layer_position)
def draw_network():
    global final_list
    for layer_index in range(len(final_list)-1):
        current_layer=final_list[layer_index]
        next_layer=final_list[layer_index+1]
        for current_index,neuron1 in enumerate(current_layer):
            x,y,act=neuron1
            for next_index,neuron2 in enumerate(next_layer):
                x1,y1,th=neuron2
                weight=all_weights[layer_index][next_index][current_index]
                signal=weight*act
                thickness=int(1+abs(signal)*12)
                if weight>0:
                    color="#22c55e"
                else:
                    color="#ef4444"
                connect_neuron(x,y,x1,y1,thickness,color)       
    for i in final_list:
        for j in i:
            x,y,act=j
            #brightness=min(255,max(0,int(abs(act)*255)))
          #  color=f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            value=max(0,min(1,abs(act)))
            r=int(120*value)
            g=int(80 + 175*value)
            b=255
            color=f"#{r:02x}{g:02x}{b:02x}"
            draw_neuron(x,y,radius,color,act)
            layer_index=final_list.index(i)
            neuron_index=i.index(j)
            if layer_index!=0:
                bias=all_biases[layer_index-1][neuron_index]
                canvas.create_text(x,y+43,text=f"b:{bias:.2f}",fill="white",font=("Segoe UI",10,"bold"))
def update_network(value=None):
    global final_list
    input_values=[]
    input_values=[slider.get() for slider in sliders]
    for i in range(len(input_values)):
        x=final_list[0][i][0]
        y=final_list[0][i][1]
        final_list[0][i]=(x,y,input_values[i])
    
    forward_propagation()
    canvas.delete("all")
    draw_network()
sliders=[]
def create_slider():
    for widget in slider_frame.winfo_children():
        widget.destroy()
    sliders.clear()
    for i in range(layers[0]):
        mini_frame=ctk.CTkFrame(slider_frame,fg_color="transparent")
        mini_frame.pack(fill="x",pady=8)
        label=ctk.CTkLabel(mini_frame,text=f"Input{i+1}",font=("Inter",11))
        label.pack(anchor="w")
        slider=ctk.CTkSlider(mini_frame,from_=-1,to=1,number_of_steps=200,command=update_network)
        slider.pack(fill="x",pady=5)
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

def forward_propagation():
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
    output_layer=final_list[-1]
    for i,neuron in enumerate(output_layer):
        activation=neuron[2]
        output_labels[i].configure(text=f"Neuron {i+1}: {activation:.3f}")
def generate_bias():
    global all_biases
    all_biases=[]
    for layer_index in range(1,len(layers)):
        
        layer_biases=[]
        for neuron in range(layers[layer_index]):
            layer_biases.append(random.uniform(-1,1))
        all_biases.append(layer_biases)
def regen_weights():
    generate_weights()
    generate_bias()
    update_network()
sigmoid_button=ctk.CTkButton(sidebar,text="Sigmoid",command=use_sigmoid,font=("Inter",11))
sigmoid_button.pack(pady=8,padx=20,fill="x")
relu_button=ctk.CTkButton(sidebar,text="reLU",command=use_relu,font=("Inter",11))
relu_button.pack(pady=8,padx=20,fill="x")
tanh_button=ctk.CTkButton(sidebar,text="tanh",command=use_tanh,font=("Inter",11))
tanh_button.pack(pady=8,padx=20,fill="x")
regen_weights_button=ctk.CTkButton(sidebar,text="Randomize Network",command=regen_weights,font=("Inter",11),fg_color="#2563eb",height=40,corner_radius=12)
regen_weights_button.pack(pady=8,padx=20,fill="x")
generate_network()
generate_weights()
generate_bias()
create_slider()
create_output_labels()
forward_propagation()
draw_network()
print(len(output_labels))
print(len(final_list[-1]))
root.mainloop()
