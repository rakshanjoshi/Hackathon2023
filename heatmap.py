import random
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Creating an object Visit which randomly generates a serial code, museum entry/exit times, room entry/exit times, and a visted room number
# These times are generated to represent visits occurring during a 120-minute (2 hour) window

class Visit:
    def __init__(self):
        self.serialNumber = chr(random.randint(65,90)) + chr(random.randint(65,90)) + chr(random.randint(65,90)) + chr(random.randint(65,90))
        self.roomNumber = random.randint(1,6)
        self.museumEntry = random.randint(0, 100)
        self.museumExit = random.randint(self.museumEntry, 120)
        while self.museumExit < self.museumEntry + 10:
            self.museumExit = random.randint(self.museumEntry, 120)        
        self.roomEntry = random.randint(self.museumEntry, self.museumExit - 5)
        self.roomExit = random.randint(self.roomEntry, self.museumExit)
        while self.roomExit < self.roomEntry + 5:
            self.roomExit = random.randint(self.roomEntry, self.museumExit)
        
visitors = []  
for i in range(200):      
    v = Visit()
    visitors.append(v)
# Generating and storing 200 visitors

members = 0
rooms = [0] * 6
membersData = []
roomsData = []

for minute in range(121):
    for visitor in visitors:
        if minute == visitor.museumEntry:
            members += 1
        if minute == visitor.museumExit:
            members -= 1
        if minute == visitor.roomEntry:
            rooms[visitor.roomNumber - 1] += 1
        if minute == visitor.roomExit:
            rooms[visitor.roomNumber - 1] -= 1
    room = copy.deepcopy(rooms)
    roomsData.append(room)
    membersData.append(members)

# Collecting data for each minute of the demo, to later be used as frames in a heatmap animation

roomsData = np.array(roomsData)
fig, ax = plt.subplots()

# Creating a frame of the animation by constructing a static heatmap plot for a specific minute
def animate(minute):
    ax.clear()
    room_counts = roomsData[minute]
    heatmap_data = room_counts.reshape(1, -1)
    ax.imshow(heatmap_data, cmap='hot_r', aspect='auto', vmin=0, vmax=15)
    ax.set_xlabel('Room Number')
    ax.set_xticks(np.arange(6))
    ax.set_xticklabels(np.arange(6) + 1)
    ax.set_title(f"Heatmap during minute {minute}")
    ax.text(0.5, 0.3, f"Total Members in Museum: {membersData[minute]}", transform=ax.transAxes, ha='center')
    ax.text(0.5, 0.2, f"Total Members in Museum Rooms: {sum(room_counts)}", transform=ax.transAxes, ha='center')
    ax.text(0.085, 0.8, f"{room_counts[0]}", transform=ax.transAxes, ha='center')
    ax.text(0.25, 0.8, f"{room_counts[1]}", transform=ax.transAxes, ha='center')
    ax.text(0.415, 0.8, f"{room_counts[2]}", transform=ax.transAxes, ha='center')
    ax.text(0.58, 0.8, f"{room_counts[3]}", transform=ax.transAxes, ha='center')
    ax.text(0.745, 0.8, f"{room_counts[4]}", transform=ax.transAxes, ha='center')
    ax.text(0.91, 0.8, f"{room_counts[5]}", transform=ax.transAxes, ha='center')
    ax.set_yticklabels([])

# Sequentially displaying each frame to create a chronological animation of the heatmap
anim = animation.FuncAnimation(fig, animate, frames=range(len(roomsData)), interval=200, repeat = False)
plt.show()
