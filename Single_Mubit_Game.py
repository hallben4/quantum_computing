#!/usr/bin/env python
# coding: utf-8

# In[2]:


import simpleaudio as sa
import numpy as np
from qiskit import *
from qiskit.visualization import plot_bloch_multivector, circuit_drawer
from PIL import ImageTk, Image
import tkinter as tk
import qutip
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

pi = np.pi

def sound(circ,note): 

    if (note == 'C'):
        f = 440*2**(-9/12)
    if (note == 'C#') or (note == 'Db'):
        f = 440*2**(-8/12)
    if (note == 'D'):
        f = 440*2**(-7/12)
    if (note == 'D#') or (note == 'Eb'):
        f = 440*2**(-6/12)
    if (note == 'E'):
        f = 440*2**(-5/12)
    if (note == 'F'):
        f = 440*2**(-4/12)
    if (note == 'F#') or (note == 'Gb'):
        f = 440*2**(-3/12)
    if (note == 'G'):
        f = 440*2**(-2/12)
    if (note == 'G#') or (note == 'Ab'):
        f = 440*2**(-1/12)
    if (note == 'A'):
        f = 440*2**(0/12)
    if (note == 'A#') or (note == 'Bb'):
        f = 440*2**(1/12)
    if (note == 'B'):
        f = 440*2**(2/12)
    
    backend = BasicAer.get_backend('statevector_simulator')
    result = execute(circ, backend).result()
    sv = result.get_statevector()
    theta = np.real(2*np.arccos(sv[0]))
    phi = np.real(np.angle(sv[1]))
    if phi < 0:
        phi = 2*pi + phi
      
    fs = 44100  # 44100 samples per second
    seconds = 0.5  # Note duration of 2 seconds
    t = np.linspace(0, seconds, seconds * fs, False) # Generate array with seconds*sample_rate steps

    # Create sound
    left =  (np.cos(theta/2))*np.sin(f*t*2*pi)
    right = (np.sin(theta/2))*np.sin(2**(phi/(2*np.pi))*f*t*2*pi+pi/2) 
    
    note = np.dstack((left,right))[0]

    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = audio.astype(np.int16) # Convert to 16-bit data
    
    # Playback
    play_obj = sa.play_buffer(audio, 2, 2, fs)
    play_obj.wait_done()

q = QuantumRegister(1, 'q')
circ = QuantumCircuit(q)

root = tk.Tk()
root.title('Mubits')
root.geometry("400x400")

backend = BasicAer.get_backend('statevector_simulator')
result = execute(circ, backend).result()
sv = result.get_statevector()
fig = plot_bloch_multivector(sv)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().place(x = 50,y = 50)

entry_list = ['c','C','d','D','e','f','F','g','G','a','A','b']
note_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

head = tk.Text(root)
head.insert(tk.INSERT, 'One Qubit')
head.place(x = 165,y = 10,height = 30,width = 80)

text = tk.Text(root)
text.insert(tk.INSERT, note_list[0])
text.place(x = 20,y = 30,height = 30,width = 30)
    
def key_press(event): 

    event.char = event.keysym
    if event.char == 'h':
        circ.h(q[0])
    if event.char == '1':
        circ.x(q[0])
    if event.char == '2':
        circ.y(q[0])
    if event.char == '3':
        circ.z(q[0])
    if event.char == 'x':
        circ.rx(pi/6,q[0])
    if event.char == 'y':
        circ.ry(pi/6,q[0])
    if event.char == 'z':
        circ.rz(pi/6,q[0])
    if event.char == 'X':
        circ.rx(-pi/6,q[0])
    if event.char == 'Y':
        circ.ry(-pi/6,q[0])
    if event.char == 'Z':
        circ.rz(-pi/6,q[0])
        
    for i in range(12):
        if event.char == entry_list[i]:
            text.delete(1.0,tk.END)
            text.insert(tk.INSERT, note_list[i])  
            sound(circ,note_list[i]) 

    backend = BasicAer.get_backend('statevector_simulator')
    result = execute(circ, backend).result()
    sv = result.get_statevector()
    fig = plot_bloch_multivector(sv)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x = 50,y = 50)

root.bind('<Key>', lambda a : key_press(a)) 

root.lift()
root.attributes('-topmost',True)
root.mainloop()

