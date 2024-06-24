# Used to display images and videos, but mainly the latter.
# This code was taken from ChatCPT

import tkinter as tk
from PIL import ImageTk
from video import Video

def display(animation: Video) -> None:
    
    # Create a Tkinter window
    root = tk.Tk()
    root.title(animation.file_name)

    # Create a label to display the frames
    label = tk.Label(root)
    label.pack()

    # Extract frames from the GIF
    frames = animation.frames

    # Start the animation
    update_frame(frames, 0, label, root)

    # Run the Tkinter event loop
    root.mainloop()

# Function to update frames
def update_frame(frames, frame_number, label, root):
    frame = frames[frame_number].source
    frame_image = ImageTk.PhotoImage(frame)
    label.config(image=frame_image)
    label.image = frame_image
    frame_number = (frame_number + 1) % len(frames)
    root.after(100, update_frame, frames, frame_number, label, root)

