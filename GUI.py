import tkinter as tk
from QRGenerationv2 import QR_Generation  
from PIL import Image, ImageTk 
from tkinter import PhotoImage
from QRGenerationv2 import create_qr_image
from image import create_qr_image2, create_qr_image3
from tkinter import Toplevel, StringVar, Radiobutton, Button
root = tk.Tk()
root.geometry("600x600")
root.title("GUI for QR Code")
import os
qr_image_label = None
qr_tk_image = None  
dark_mode_enabled = False  

img_path2 = "c:/Users/hassa/QR_Code_v2/qr_withfinderpatterns.png"
img_path3 = "c:/Users/hassa/QR_Code_v2/qr_with_timing_patterns.png"
img_path4 = "c:/Users/hassa/QR_Code_v2/qr_with_reserve_info.png"
img_path5 = "c:/Users/hassa/QR_Code_v2/qr_with_data_bits_v1.png"
img_path6 = "c:/Users/hassa/QR_Code_v2/qr_with_format_bits.png"
selected_color_hex = (0, 0, 0) 

def button_clicked():
    user_input = T.get("1.0", "end").strip() 
    if user_input:
        try:
            qr = QR_Generation(user_input) 
            final_matrix = qr.generate_final_bit_stream()  # Get final matrix

            shape = qr_shape_var.get()  
            if shape == "square":
                img = create_qr_image(final_matrix, color=selected_color_hex)
            elif shape == "circle":
                img = create_qr_image2(final_matrix, color=selected_color_hex)
            elif shape == "diamond":
                img = create_qr_image3(final_matrix, color=selected_color_hex)
            else:
                raise ValueError("Invalid QR shape selected.")
           
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            img_path = os.path.join(downloads_path, "generated_qr.png")
            img.save(img_path)
            status_label.config(text=f"QR code saved to: {img_path}", fg="green")
            show_qr(img_path)  # Update image in UI
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

def colour_qr():
    global selected_color_hex
    color_window = tk.Toplevel()
    color_window.title("Choose QR Code Color")
    color_window.geometry("400x200")

    colors = {
        "Black": (0, 0, 0),
        "Red": (255, 0, 0),
        "Green": (0, 255, 0),
        "Blue": (0, 0, 255),
        "Purple": (128, 0, 128),
        "Orange": (255, 165, 0),
        "Yellow": (255, 255, 0),
        "Cyan": (0, 255, 255),
    }

    def rgb_to_hex(rgb_tuple):
        return '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)

    def set_color(color_name):
        global selected_color_hex
        selected_color_hex = colors[color_name]  # store as RGB tuple for image creation
        print(f"Selected color: {color_name} ({selected_color_hex})")
        color_window.destroy()

    row = 0
    col = 0
    for name, rgb in colors.items():
        hex_code = rgb_to_hex(rgb)  # convert for button bg
        btn = tk.Button(color_window, bg=hex_code, width=6, height=2, command=lambda n=name: set_color(n))
        btn.grid(row=row, column=col, padx=10, pady=10)
        label = tk.Label(color_window, text=name)
        label.grid(row=row + 1, column=col)

        col += 1
        if col == 4:
            col = 0
            row += 2

def open_empty_window(img_path2, img_path3, img_path4,img_path5,img_path6):
    new_window = tk.Toplevel(root)
    new_window.title("QR Creation Slideshow")
    new_window.geometry("600x150+700+100")  # Wider window for 3 images

    try:
        # Load and resize images
        img1 = Image.open(img_path2).resize((100, 100))
        img2 = Image.open(img_path3).resize((100, 100))
        img3 = Image.open(img_path4).resize((100, 100))
        img4 = Image.open(img_path5).resize((100,100))
        img5 = Image.open(img_path6).resize((100,100))

        qr_image1 = ImageTk.PhotoImage(img1)
        qr_image2 = ImageTk.PhotoImage(img2)
        qr_image3 = ImageTk.PhotoImage(img3)
        qr_image4 = ImageTk.PhotoImage(img4)
        qr_image5 = ImageTk.PhotoImage(img5)

        # First image label (far left)
        label1 = tk.Label(new_window, image=qr_image1)
        label1.image = qr_image1
        label1.place(x=5, y=5)

        # Second image label (middle)
        label2 = tk.Label(new_window, image=qr_image2)
        label2.image = qr_image2
        label2.place(x=115, y=5)

        # Third image label (right of both)
        label3 = tk.Label(new_window, image=qr_image3)
        label3.image = qr_image3
        label3.place(x=225, y=5)

        label4 = tk.Label(new_window, image=qr_image4)
        label4.image = qr_image4
        label4.place(x=335,y=5)

        
        label5 = tk.Label(new_window, image=qr_image5)
        label5.image = qr_image5
        label5.place(x=440,y=5)

    except Exception as e:
        error_label = tk.Label(new_window, text=f"Error loading images: {str(e)}", fg="red")
        error_label.pack(pady=20)

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
                    command=lambda: open_empty_window(img_path2,img_path3,img_path4,img_path5,img_path6),
                    bg="yellow",
                    fg="black",
                    font =("Arial",12),
                    height=2,
                    width=17)
button3.place(x=70,y=70)


button4 = tk.Button(root,
                    text="Change Colour",
                    command=colour_qr,
                    bg="blue",
                    fg="black",
                    font =("Arial",12),
                    height=2,
                    width=17)
button4.place(x=70,y=35)



def toggle_dark_mode():
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled

    if dark_mode_enabled:
        bg_color ="#2e2e2e"
        fg_color = "white"
        entry_bg = "#3c3c3c"
    else:
        bg_color = "lightgray"
        fg_color = "black"
        entry_bg = "white"

    root.config(bg=bg_color)

    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            if widget.cget("text") == "Toggle Dark Mode":
                widget.config(bg="#444" if dark_mode_enabled else "SystemButtonFace", fg=fg_color)
            continue  

        try:
            widget.config(bg=bg_color, fg=fg_color)
        except:
            pass

        if isinstance(widget, tk.Text):
            widget.config(bg=entry_bg, fg=fg_color)

# This variable will hold the user's choice and be passed to your QR generator later
qr_shape_var = StringVar(value="square")  # default to square

def choose_qr_shape():
    def apply_choice():
        selected_shape = shape_choice.get()
        qr_shape_var.set(selected_shape)
        popup.destroy()
    
    popup = Toplevel(root)
    popup.title("Select QR Code Shape")
    popup.geometry("250x150")
    popup.grab_set()

    shape_choice = StringVar(value=qr_shape_var.get())

    Radiobutton(popup, text="Square", variable=shape_choice, value="square").pack(anchor="w", padx=20, pady=5)
    Radiobutton(popup, text="Circle", variable=shape_choice, value="circle").pack(anchor="w", padx=20, pady=5)
    Radiobutton(popup, text="Diamond", variable=shape_choice, value="diamond").pack(anchor="w", padx=20, pady=5)

    Button(popup, text="Apply", command=apply_choice).pack(pady=10)

dark_mode_btn = tk.Button(root, text="Toggle Dark Mode", bg="gray", fg="white", command=toggle_dark_mode)
dark_mode_btn.place(x=100, y=270)  # Adjust position as needed

change_shape_btn = tk.Button(root, text="Change qr shape", bg="gray", fg="white", command=choose_qr_shape)
change_shape_btn.place(x=100,y=240)


status_label = tk.Label(root, text="", fg="blue", font=("Arial", 10))
status_label.place(x=100, y=550)

root.mainloop()
