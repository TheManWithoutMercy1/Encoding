import tkinter as tk
from QRGenerationv2 import QR_Generation  
from PIL import Image, ImageTk 
from tkinter import PhotoImage

root = tk.Tk()
root.geometry("600x600")
root.title("GUI for QR Code")

qr_image_label = None
qr_tk_image = None  

def button_clicked():
    user_input = T.get("1.0", "end").strip() 
    if user_input:
        try:
            qr = QR_Generation(user_input) 
            img_path = qr.generate_final_bit_stream() 
            status_label.config(text=f"QR code saved to: {img_path}", fg="green")
            show_qr(img_path)
           
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="red")
    else:
        status_label.config(text="Please enter some text first.", fg="red")

def clear_text():
    T.delete("1.0", "end")
    status_label.config(text="Text cleared.", fg="blue")

def show_qr(img_path):
    global qr_tk_image, qr_image_label

    img = Image.open(img_path)
    img = img.resize((135,135))  # Optional resizing
    qr_tk_image = ImageTk.PhotoImage(img)  # Keep reference alive!

    if qr_image_label is None:
        qr_image_label = tk.Label(root, image=qr_tk_image)
        qr_image_label.place(x=370, y=120)  # Adjust placement as needed
    else:
        qr_image_label.config(image=qr_tk_image)

def open_empty_window():
    # Create a new top-level window
    new_window = tk.Toplevel(root)
    new_window.title("QR Creation Slideshow")
    new_window.geometry("400x400+700+100")  # Width x Height + X + Y

    # Optional: Add a label inside the window
    label = tk.Label(new_window, text="This is a new empty window.", font=("Arial", 14))
    label.pack(pady=20)


heading_label = tk.Label(root, text="QR Code Generator", font=("Helvetica", 24))
heading_label.pack()

content_label = tk.Label(root, text="This is a basic GUI created using Tkinter.")
content_label.pack()

box_label = tk.Label(root, 
                     text="Enter text within the textbox.\nPress 'Clear All' to remove all text and 'Get QR Code' to generate a QR code.",
                     wraplength=400, 
                     justify="left")
box_label.place(x=70, y=250)




T = tk.Text(root, height=15, width=40)
T.place(x=100, y=320)


button = tk.Button(root, 
                   text="Get QR Code", 
                   command=button_clicked,
                   bg="green",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   width=17)
button.place(x=70, y=120)

button2 = tk.Button(root, 
                   text="Clear All", 
                   command=clear_text,
                   bg="red",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   width=17)
button2.place(x=70, y=170)


button3 = tk.Button(root,
                    text="QR creation slideshow",
                    command=open_empty_window,
                    bg="yellow",
                    fg="black",
                    font =("Arial",12),
                    height=2,
                    width=17)
button3.place(x=70,y=70)

status_label = tk.Label(root, text="", fg="blue", font=("Arial", 10))
status_label.place(x=100, y=550)

root.mainloop()
