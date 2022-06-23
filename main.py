# Heartrate simulator version 3.0

# importing modules
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from math import *
import math

class RunningTimer: 
    def __init__(self): #
        # defining the gui elements
        self.root = tk.Tk()
        self.root.geometry("600x700")
        self.root.title("Puls simulator") #
        
        self.root.seconds_title_label = tk.Label(text="Sekunder", font=("Cascadia Mono", 15))
        self.root.seconds_title_label.grid(row=1, column=1, padx=50, pady=(25, 0))

        # variable storing time
        self.seconds = StringVar()

        # set the default start time to 0
        self.seconds = 0

        # varible to store total time
        self.total_seconds = 0

        # create a label to display the number of seconds
        self.root.seconds_label = tk.Label(text=self.seconds)
        self.root.seconds_label.grid(row=2, column=1, padx=50)

        # variable storing heartrate
        self.heartrate = float()
        
        # set default value for heartrate
        self.heartrate = 90

        # set the minimum pulse value
        self.minimum_heartrate = 90

        # set the maximum pulse value to
        self.maximum_heartrate = 186

        # set the clock speed in ms
        self.clock_speed = 1000

        # define an array to store statistical data on the heartrate
        self.heartrate_history = [self.heartrate]

        # define an array to store the statistical data on seconds
        self.seconds_history = [0]

        # create a label to describe the heartrate value
        self.root.heartrate_title_label = tk.Label(text="Puls", font=("Cascadia Mono", 15))
        self.root.heartrate_title_label.grid(row=3, column=1, padx=50, pady=(25, 0))

        # create a label to show the pulse value
        self.root.heartrate_label = tk.Label(text=self.heartrate)
        self.root.heartrate_label.grid(row=5, column=1, padx=50)

        # insert a button to start and stop the running simulation
        self.root.running_toggle = tk.Button(text="Start løping", command=self.running_button_callback)
        self.root.running_toggle.grid(row=6, column=1, padx=50, pady=(25,0))

        # create a label to show speed title
        self.root.speed_title_label = tk.Label(text="Hastighet")
        self.root.speed_title_label.grid(row=9, column=1, padx=50, pady=(25,0))

        # insert a button to change clock speed
        self.root.speed_toggle = tk.Button(text="5x", command=self.speed_button_callback)
        self.root.speed_toggle.grid(row=10, column=1, padx=50)

        # define a variable to know if we are running or not (default is not running)
        self.running = False

        # define a varible to know if the clock speed is changed (default is not changed)
        self.speed_changed = False

        # define a variable to keep track of the timer function (running_engine())
        self.is_engine_running = False

        # start the timer
        self.root.mainloop()

    def f(self): 
        # f(self)
        # -0.0289*self.seconds**2+3.1*self.seconds + 90 # Function

        # The derivative function of f(self)
        return self.heartrate + (-0.0578*self.seconds+3.1)

    def g(self): 
        # g(self) =
        # 0.08246*self.seconds+167.73864

        # The derivative function of g(self)
        pulse = self.heartrate + 0.08246

        if pulse > self.maximum_heartrate: 
            pulse = self.maximum_heartrate

        return pulse

    def h(self): 
        print(self.heartrate)

        # h(self)
        # 176.5264*0.9979**self.seconds

        # The derivative function of h(self)
        pulse = self.heartrate + (-0.3711*math.e**(-0.0021*self.seconds))

        if pulse > self.minimum_heartrate: 
            return pulse
        else: 
            return self.minimum_heartrate

    def render_history(self): 
        heartrate_history_data = {'Sekunder' : self.seconds_history,
                'Puls' : self.heartrate_history}

        df = DataFrame(heartrate_history_data, columns=['Sekunder', 'Puls'])
        
        heartrate_figure = plt.Figure(figsize=(5,4), dpi=100)
        ax = heartrate_figure.add_subplot(111)
        line = FigureCanvasTkAgg(heartrate_figure, self.root)
        line.get_tk_widget().grid(row=8, column=1, padx=50, pady=(15,0))
        df = df[['Sekunder','Puls']].groupby('Sekunder').sum()
        df.plot(kind='line', linewidth=2, legend=True, ax=ax, color='r',marker='', fontsize=10)
        ax.set_title('Puls over tid')

    def running_button_callback(self):
        # reset the seconds counter 
        self.seconds = 0

        # Change running status
        if self.running == True: 
            self.running = False
            self.root.running_toggle.config(text="Start løping")
        else:
            self.running = True
            self.root.running_toggle.config(text="Stopp løping")
            if (self.is_engine_running == False):
                self.is_engine_running = True
                self.running_engine()

    def speed_button_callback(self):
        # set the clock speed to 500 ms
        self.clock_speed = 200

        if self.speed_changed == True: 
            self.speed_changed = False
            self.root.speed_toggle.config(text="5x")
            self.clock_speed = 1000
        else:
            self.speed_changed = True
            self.root.speed_toggle.config(text="1x")
            if self.clock_speed > 1000:
                self.clock_speed = 200

    def running_engine(self): #

        # increment the amount of seconds
        self.seconds += 1

        # update the seconds label 
        self.root.seconds_label.config(text=self.seconds)

        # increase the total number of running seconds 
        self.total_seconds += 1

        # calculate the current heartrate after X seconds
        if self.running == False:
            y = round(self.h(), 2)
            print("Bruker h(x)")
        elif self.heartrate > 171.54346 and self.running == True: # Changes between different functions based on the value of x
            y = round(self.g(), 2) # 2 determines how the float will be rounded
            print("Bruker g(x)")
        else:
            y = round(self.f(), 2) # 2 determines how the float will be rounded
            print("Bruker f(x)")

        # update the heartrate label with the new heartrate value
        self.root.heartrate_label.config(text=y)

        # update the heartrate variable label
        self.heartrate = y

        # add the new heartrate to the heartrate history and seconds to the seconds history
        self.heartrate_history.append(y)
        self.seconds_history.append(self.total_seconds)
        
        # Update and render the graph
        self.render_history()

        if self.running == True:
            print("Running forward")
            print(self.seconds)
            print(self.heartrate)

        else: 
            print("Not running")
        self.root.after(self.clock_speed, self.running_engine) #

if __name__ == "__main__":
    running_gui = RunningTimer()