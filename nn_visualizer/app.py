import tkinter as tk
root=tk.Tk()
root.geometry("500x400")
canvas=tk.Canvas(root,bg="#757575",height=380,width=450)
def draw_neuron(x,y,radius):
    canvas.create_oval(x-radius,y-radius,x+radius,y+radius,fill="white")
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
        draw_neuron(x,y,r)
        layer_position.append((x,y))
    final_list.append(layer_position)
for i in range(len(final_list)-1):
    layer=final_list[i]
    for j in layer:
        x,y=j
        for k in final_list[i+1]:
            x1,y1=k
            connect_neuron(x,y,x1,y1)
        
canvas.pack()

root.mainloop()
