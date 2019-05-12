import tkinter as tk

class Display(tk.Frame):
    #Classe qui gère l'affichage à l'écran
    def __init__(self,parent,data,step):
        tk.Frame.__init__(self,parent)
        self.parent=parent
        self.step=step
        self.canvas=tk.Canvas(self.parent,width=800,height=450,bg='blue')
        self.canvas.pack()
        self.canvas.create_polygon(185,370,215,370,215,400,185,400,fill="red",outline="pink",width=5,tags=("h0","s0","cube","no_counter"))
        self.canvas.create_rectangle(0,400,800,450,fill="grey",width=3,outline="white",tags=("h400","s3","sol","no_counter"))
        self.counter=0
        self.shapes=([0,400],[0,0,40,0,40,40,0,40])
        self.data=self.decode(data)
        self.lenght=len(self.data)-1

    def create_object(self,shape_property):
        shape,height,x=shape_property
        points=self.shapes[shape]
        m=(len(points))//2
        x=[points[2*i]+x for i in range(m)]
        y=[height+points[2*i+1] for i in range(m)]
        points=[(x[i],y[i]) for i in range(m)]
        self.canvas.create_polygon(points,fill="purple",outline="white",width=2,tags=("h"+str(height),"s"+str(shape),"map","c"+str(self.counter)))

    def move(self):
        self.canvas.move("map",self.step,0)
        instruction=self.data[self.counter]
        self.create_object(instruction)
        self.canvas.delete("c"+str(self.counter-720//self.step))
        self.counter+=1

    def Point(self,x,y):
        tag=self.canvas.gettags(max((1,)+self.canvas.find_overlapping(x,y,x,y)))
        if len(tag)==4:
            return int(tag[0][1:]),int(tag[1][1:])
        else:
            return 0,0
    def cube(self,y):
        pos=int(self.canvas.coords('cube')[7])
        self.canvas.move('cube',0,y-pos)

    def Get_Sensor(self,x,y):
        return [self.Point(x-15,y),self.Point(x+15,y),self.Point(x+15,y-30),self.Point(x-15,y-30)]
    
    def decode(self,data):
        texture=list()
        lines=data.split("\n")
        for line in lines:
            instructions=line.split("+")
            l=len(instructions)
            for i in range(l):
                instruction=instructions[i].split("-")
                texture.append((int(instruction[0]),int(instruction[1]),760+i*self.step))
            for i in range(10-l):
                texture.append((0,0,760+(l+i)*self.step))
        return texture


class Movement():

    def __init__(self):
        clean(root)
        self.vy=0
        self.y=395
        self.stop=False
        self.display=Display(root,data,-4)
        self.display.pack(side="top", fill="both", expand=True)
        root.bind("<space>",self.jump)
        self.append()
 
    def append(self):
        self.sensor=self.display.Get_Sensor(200,self.y)
        self.bottom_sensor=max(self.sensor[0][0],self.sensor[1][0])
        #print(self.y)      
        self.display.move()

        
        self.y-=int((3/5)*self.vy)
        self.vy-=1

        self.display.cube(self.y)
        

        if self.bottom_sensor:
            self.y=self.bottom_sensor
            self.vy=0

        
        if self.display.counter!=self.display.lenght and not self.stop:
            root.after(13,self.append)

    def jump(self,event):
        print("jump")
        self.vy=20
        self.y-=5



def clean(parent):
    for i in parent.winfo_children():
        i.destroy()
        
file=open("map.txt","r")
data=file.read()
file.close()


root=tk.Tk()
root.title("Geometry Dash")


Movement()
root.mainloop()

