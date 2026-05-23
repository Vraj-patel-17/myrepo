import tkinter as tk
import random
import numpy as np
root=tk.Tk()
root.geometry("1200x700")
slider_frame=tk.Frame(root)
slider_frame.pack(pady=10)   
canvas=tk.Canvas(root,bg="#dfe6e9",height=600,width=1200)
layers=[3,4,2]
r=30
def draw_neuron(x,y,radius,color):
    canvas.create_oval(x-radius,y-radius,x+radius,y+radius,fill=color)
def connect_neuron(x1,y1,x2,y2,thickness):
    canvas.create_line(x1,y1,x2,y2,fill="black",width=thickness)
def generate_network():
    
    global layers
    x_positions=[250,450,650]
    global r
    spacing=100
    center=300
    global final_list
    final_list=[]
    for layer_index in range(len(layers)):
        layer_position=[]
        neurons=layers[layer_index]
        total_height=spacing*(neurons-1)
        start_y=center-total_height//2
        x=x_positions[layer_index]
        for i in range(neurons):
            y=start_y +i*spacing
            activation=random.random()
            #draw_neuron(x,y,r,color)
            layer_position.append((x,y,0))
        final_list.append(layer_position)
def draw_network():
    global final_list
    for i in range(len(final_list)-1):
        layer=final_list[i]
        for j in layer:
            x,y,_=j
            for k in final_list[i+1]:
                x1,y1,th=k
                thickness=abs(th)*5
                connect_neuron(x,y,x1,y1,thickness)
    for i in final_list:
        for j in i:
            x,y,act=j
            brightness=int(abs(act)*255)
            color=f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            draw_neuron(x,y,r,color)
def update_network(value):
    global input_values
    input_values=[slider.get() for slider in sliders]
    canvas.delete("all")
    forward_propagation()
    draw_network()
sliders=[]
for i in range(1,(layers[0])+1):
    mini_frame=tk.Frame(slider_frame,bg="#dfe6e9")
    mini_frame.pack(side="left",padx=20)
    slider=tk.Scale(mini_frame,from_=-1,to=1,resolution=0.01,orient="horizontal",command=update_network)
    slider.pack()
    label=tk.Label(mini_frame,text=f"Input{i}",bg="#dfe6e9")
    label.pack()
    sliders.append(slider)
def forward_propagation():
    global final_list
    weight_value=[]
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
        final_list[-1][i]=(x,y,z_out_value[i])


generate_network()
canvas.pack()
root.mainloop()
