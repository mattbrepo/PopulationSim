import tkinter
import customtkinter
import PopulationSim
import threading

# -- Global
root = customtkinter.CTk()
slider_pop_size = tkinter.IntVar()
slider_pop_size.set(PopulationSim.POP_SIZE)
slider_simulation_step = tkinter.DoubleVar()
slider_simulation_step.set(PopulationSim.SIMULATION_STEP_TIME)
slider_speed = tkinter.DoubleVar()
slider_speed.set(PopulationSim.SPEED)
slider_perc_female = tkinter.DoubleVar()
slider_perc_female.set(PopulationSim.PERC_FEMALE)
slider_chance_offspring = tkinter.DoubleVar()
slider_chance_offspring.set(PopulationSim.CHANCE_OFFSPRING)
thr = None

# -- Functions
def add_slider_control(root, y, name, value, min, max):
  label = customtkinter.CTkLabel(master=root, text=name)
  label.place(relx=0.2, rely=y, anchor=tkinter.CENTER)
  slider = customtkinter.CTkSlider(master=root, from_=min, to=max, variable=value)
  slider.place(relx=0.5, rely=y, anchor=tkinter.CENTER)
  labelVal = customtkinter.CTkLabel(master=root, textvariable=value)
  labelVal.place(relx=0.8, rely=y, anchor=tkinter.CENTER)
  return slider

def slider_pop_size_event(event):
  PopulationSim.POP_SIZE = slider_pop_size.get()

def slider_simulation_step_event(event):
  PopulationSim.SIMULATION_STEP_TIME = slider_simulation_step.get()
  
def slider_speed_event(event):
  PopulationSim.SPEED = slider_speed.get()

def slider_perc_female_event(event):
  PopulationSim.PERC_FEMALE = slider_perc_female.get()
  
def slider_chance_offspring_event(event):
  PopulationSim.CHANCE_OFFSPRING = slider_chance_offspring.get()

def button_start_event():
  global thr
  if thr == None or not thr.is_alive():
    thr = threading.Thread(target=PopulationSim.run_sim, args=(), kwargs={})
    thr.start()

#
# MAIN
#

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root.geometry("700x400")
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=0, padx=0, fill="both", expand=True)

# input sliders
slider = add_slider_control(root, 0.1, "Initial population", slider_pop_size, 1, 100)
slider.bind("<ButtonRelease-1>", slider_pop_size_event)

slider = add_slider_control(root, 0.2, "Simulation step", slider_simulation_step, 1 / 30, 1)
slider.bind("<ButtonRelease-1>", slider_simulation_step_event)

slider = add_slider_control(root, 0.3, "Individual speed", slider_speed, 0.5, 5)
slider.bind("<ButtonRelease-1>", slider_speed_event)

slider = add_slider_control(root, 0.4, "Percentage female", slider_perc_female, 0.001, 0.999)
slider.bind("<ButtonRelease-1>", slider_perc_female_event)

slider = add_slider_control(root, 0.5, "Chance offspring", slider_chance_offspring, 0, 1)
slider.bind("<ButtonRelease-1>", slider_chance_offspring_event)

# start button
button = customtkinter.CTkButton(master=root, text="Start", command=button_start_event)
button.pack(padx=0, pady=40)

root.mainloop()