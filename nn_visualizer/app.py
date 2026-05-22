import tkinter as tk
import random
import numpy as np
root=tk.Tk()
root.geometry("500x400")
canvas=tk.Canvas(root,bg="#FFFAFA",height=380,width=450)
def draw_neuron(x,y,radius,color):
    canvas.create_oval(x-radius,y-radius,x+radius,y+radius,fill=color)
def connect_neuron(x1,y1,x2,y2):
    canvas.create_line(x1,y1,x2,y2,fill="black")

layers=[3,4,2]
x_positions=[100,220,340]
r=20
spacing=70
center=180
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
for i in range(len(final_list)-1):
    layer=final_list[i]
    for j in layer:
        x,y,_=j
        for k in final_list[i+1]:
            x1,y1,_=k
            connect_neuron(x,y,x1,y1)
input_values=np.array([random.uniform(-1,1) for i in range(layers[0])])
weight_value=[]
for i in range(len(input_values)):
    x=final_list[0][i][0]
    y=final_list[0][i][1]
    final_list[0][i]=(x,y,input_values[i])
x_=final_list[1][0][0]
y_=final_list[1][0][1]
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
for i in final_list:
    for j in i:
        x,y,act=j
        brightness=int(abs(act)*255)
        color=f"#{brightness:02x}{brightness:02x}{brightness:02x}"
        draw_neuron(x,y,r,color)    

canvas.pack()
root.mainloop()
