import PIL
from PIL import ImageTk
from PIL import Image
import tkinter as tk
import threading
from threading import Thread
import base64
import numpy as np
import io
import pyrebase
import time
from datetime import datetime

# import requests

temperature1 = 0.00
temperature2 = 0.00
temperature3 = 0.00
humidity1 = 0.00
humidity2 = 0.00
humidity3 = 0.00

config = {
  "apiKey": "AIzaSyCCFz7963ExMyf2vL6dtWsSu_ybXyDNDlA",
  "authDomain": "qppd-4bcba.firebaseapp.com",
  "databaseURL": "https://qppd-4bcba-default-rtdb.firebaseio.com/",
  "storageBucket": "qppd-4bcba.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


class RPiApp:
    def __init__(self, root):

        global home_indicator, sort_indicator, kool_indicator, current_menu, update_ui
        update_ui = True
        self.root = root
        self.root.title("Tomato Sorter")
        #self.root.iconbitmap("/home/pi/Downloads/ui/icon.ico")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        self.create_options_frame()
        self.create_main_frame()

        # root.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_options_frame(self):
        global home_indicator, sort_indicator, kool_indicator
        options_frame = tk.Frame(self.root, bg="#33b09a")

        home_indicator = self.create_button(options_frame, "/home/pi/Downloads/ui/home_button.png",
                                            10, 30, 3, 30, self.show_home_page)

        sort_indicator = self.create_button(options_frame, "/home/pi/Downloads/ui/sort_button.png",
                                            10, 60, 3, 60, self.show_sort_page)
        kool_indicator = self.create_button(options_frame, "/home/pi/Downloads/ui/kool_button.png",
                                            10, 90, 3, 90, self.show_kool_page)

        self.create_exit_button(options_frame)

        options_frame.pack(side=tk.LEFT)
        options_frame.pack_propagate(False)
        options_frame.configure(width=114, height=self.root.winfo_screenheight())

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="#FFFFFF", highlightbackground="black", highlightthickness=1, highlightcolor="black")
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width=self.root.winfo_screenwidth() - 114, height=self.root.winfo_screenheight())

    def indicate2(self):
        global home_indicator, current_menu
        current_menu = 0
        home_indicator.config(bg="#bd2832")
        self.show_home_page()
        
    def indicate(self, label, page_function):
        global home_indicator, sort_indicator, kool_indicator
        home_indicator.config(bg="#33b09a")
        sort_indicator.config(bg="#33b09a")
        kool_indicator.config(bg="#33b09a")

        label.config(bg="#bd2832")
        # Call the corresponding page function
        page_function()

    def create_button(self, parent, image_path, x, y, x1, x2, page_function):
        indicator = self.create_indicator(parent, x1, x2)

        # Load the image
        original_image = Image.open(image_path)

        # Resize the image to fit within the button
        width, height = original_image.size
        max_width = 130
        max_height = 25

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = original_image

        # Convert the resized image to a PhotoImage
        image = ImageTk.PhotoImage(resized_image)

        # Create the button with the image
        btn = tk.Button(parent, image=image, bg="#33b09a",  bd=0, highlightthickness=0,
                        command=lambda: self.indicate(indicator, page_function))

        btn.config(bg='#33b09a')
        btn.place(x=x, y=y, width=94, height=25)  # Set width and height
        btn.image = image  # Retain a reference to the image to prevent garbage collection

        return indicator

    def create_indicator(self, parent, x, y):
        indicator = tk.Label(parent, text='', bg="#33b09a")
        indicator.place(x=x, y=y, height=25)
        return indicator

    def create_exit_button(self, parent):

        image_path = "/home/pi/Downloads/ui/exit_button.png"

        original_image = Image.open(image_path)

        # Resize the image to fit within the button
        width, height = original_image.size
        max_width = 130
        max_height = 25

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = original_image

        # Convert the resized image to a PhotoImage
        image = ImageTk.PhotoImage(resized_image)

        # Create the button with the image
        btn = tk.Button(parent, image=image, bg="#33b09a", bd=0, highlightthickness=0,
                        command=self.root.destroy)

        btn.config(bg='#33b09a')
        btn.place(x=10, y=120, width=94, height=25)  # Set width and height
        btn.image = image  # Retain a reference to the image to prevent garbage collection

    def show_logo(self, directory, parent, width, height):
        image = Image.open(directory)
        image = image.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(parent, image=photo, bg="white", padx=10, pady=2)
        photo_label.image = photo  # Keep a reference to avoid garbage collection
        # label = tk.Label(self.home_frame, text="Sort Page", font=('Bold', 20), bg="#FFFFFF")
        photo_label.pack(pady=2)

    def show_home_page(self):
        global current_menu, update_ui
        current_menu = 0
        update_ui = False
        # Function to display the home page content
        self.clear_main_frame()

        self.home_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.home_frame.pack(side=tk.LEFT)
        self.home_frame.pack_propagate(False)
        self.home_frame.configure(width=self.root.winfo_screenwidth() - 150, height=self.root.winfo_screenheight())

        welcome_logo_path = "/home/pi/Downloads/ui/welcome_logo.png"
        self.show_logo(welcome_logo_path, self.home_frame, 300, 60)

        # Create a frame to hold the two boxes
        self.boxes_frame = tk.Frame(self.home_frame, bg="#FFFFFF")
        self.boxes_frame.pack(fill=tk.BOTH, expand=True)

        # Create the left box
        self.left_box = tk.Frame(self.boxes_frame, bg="#fbc9cc", bd=2, highlightbackground="#b5141f",
                                 highlightthickness=2)
        self.left_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=3)
        self.boxes_frame.grid_columnconfigure(0, weight=1)  # Set weight of column 0
        self.boxes_frame.grid_rowconfigure(0, weight=1)



        # Add content to the left box
        self.left_label = tk.Label(self.left_box, text="PRESERVATION", font=('Orbitron', 10), bg="#fbc9cc")
        self.left_label.pack(padx=20, pady=3, anchor="nw")

        self.live_sensor_label = tk.Frame(self.left_box, bg="#fbc9cc")
        self.live_sensor_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=(30, 30))

        # Create the frame for sensor titles
        self.live_sensor_title_label = tk.Frame(self.left_box, bg="#fbc9cc")
        self.live_sensor_title_label.pack(padx=10, pady=3)

        # Create sensor boxes inside the live sensor label frame
        sensor_box1 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box1.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        sensor_box2 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box2.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        sensor_box3 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box3.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Create sensor title labels inside the live sensor title label frame
        sensor_title1 = tk.Label(self.live_sensor_title_label, text="Unripe", font=('Orbitron', 10), bg="#fbc9cc")
        sensor_title1.pack(side=tk.LEFT, padx=10, pady=3)

        sensor_title2 = tk.Label(self.live_sensor_title_label, text="Turning", font=('Orbitron', 10), bg="#fbc9cc")
        sensor_title2.pack(side=tk.LEFT, padx=10, pady=3)

        sensor_title3 = tk.Label(self.live_sensor_title_label, text="Ripe", font=('Orbitron', 10), bg="#fbc9cc")
        sensor_title3.pack(side=tk.LEFT, padx=10, pady=3)

        self.sensor_data_label11 = tk.Label(sensor_box1, text="0", font=('Orbitron', 15), bg="#FFFFFF",
                                           justify="center")
        self.sensor_data_label11.pack(expand=True, fill=tk.BOTH)

        self.sensor_data_label22 = tk.Label(sensor_box2, text="0", font=('Orbitron', 15), bg="#FFFFFF",
                                           justify="center")
        self.sensor_data_label22.pack(expand=True, fill=tk.BOTH)

        self.sensor_data_label33 = tk.Label(sensor_box3, text="0", font=('Orbitron', 15), bg="#FFFFFF",
                                           justify="center")
        self.sensor_data_label33.pack(expand=True, fill=tk.BOTH)

        # Create a small box with background #fbc9cc
        self.live_feed_result_box = tk.Frame(self.left_box, bg="#fbc9cc", width=50, height=50)
        self.live_feed_result_box.pack(fill=tk.BOTH, padx=50, pady=5)

        self.home_total = tk.Label(self.live_feed_result_box, text="TOTAL: ", font=('Orbitron', 10),
                                    bg="#fbc9cc",
                                    justify="center")
        self.home_total.grid(row=2, column=1, padx=(20, 20), pady=5, sticky="e")

        # Create the right box
        self.right_box = tk.Frame(self.boxes_frame, bg="#fbc9cc", bd=2, highlightbackground="#b5141f",
                                  highlightthickness=2)
        self.right_box.grid(row=0, column=1, sticky="nsew", padx=10, pady=3)
        self.boxes_frame.grid_columnconfigure(1, weight=1)  # Set weight of column 1

        # Add content to the left box
        self.left_label = tk.Label(self.right_box, text="SORTING", font=('Orbitron', 10), bg="#fbc9cc")
        self.left_label.pack(padx=20, pady=3, anchor="nw")

        self.live_sensor_label = tk.Frame(self.right_box, bg="#fbc9cc")
        self.live_sensor_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=(50, 50))

        # Create the frame for sensor titles
        self.live_sensor_title_label = tk.Frame(self.right_box, bg="#fbc9cc")
        self.live_sensor_title_label.pack(padx=10, pady=3)

        # Create sensor boxes inside the live sensor label frame
        sensor_box1 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box1.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        sensor_box2 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box2.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        sensor_box3 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box3.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Create sensor title labels inside the live sensor title label frame
        sensor_title1 = tk.Label(self.live_sensor_title_label, text="Unripe", font=('Orbitron', 10), bg="#fbc9cc")
        sensor_title1.pack(side=tk.LEFT, padx=10, pady=3)

        sensor_title2 = tk.Label(self.live_sensor_title_label, text="Turning", font=('Orbitron', 10), bg="#fbc9cc")
        sensor_title2.pack(side=tk.LEFT, padx=10, pady=3)

        sensor_title3 = tk.Label(self.live_sensor_title_label, text="Ripe", font=('Orbitron', 10), bg="#fbc9cc")
        sensor_title3.pack(side=tk.LEFT, padx=10, pady=3)

        self.sensor_data_label111 = tk.Label(sensor_box1, text="0°C", font=('Orbitron', 15), bg="#FFFFFF",
                                           justify="center")
        self.sensor_data_label111.pack(expand=True, fill=tk.BOTH)

        self.sensor_data_label222 = tk.Label(sensor_box2, text="0°C", font=('Orbitron', 15), bg="#FFFFFF",
                                           justify="center")
        self.sensor_data_label222.pack(expand=True, fill=tk.BOTH)

        self.sensor_data_label333 = tk.Label(sensor_box3, text="0°C", font=('Orbitron', 15), bg="#FFFFFF",
                                           justify="center")
        self.sensor_data_label333.pack(expand=True, fill=tk.BOTH)

        # Create a small box with background #fbc9cc
        self.live_feed_result_box = tk.Frame(self.right_box, bg="#fbc9cc", width=100, height=50)
        self.live_feed_result_box.pack(fill=tk.BOTH, padx=50, pady=5)

        self.home_timer_label = tk.Label(self.live_feed_result_box, text="TIME RUNNING: ", font=('Orbitron', 10),
                                    bg="#fbc9cc",
                                    justify="center")
        self.home_timer_label.grid(row=2, column=1, padx=(20, 20), pady=5, sticky="e")
        
        update_ui = True


    def show_sort_page(self):
        global current_menu, update_ui
        current_menu = 1
        update_ui = False
        # Function to display the sort page content
        self.clear_main_frame()
        
        sorting = db.child("sorter").child("operation").child("operate").child("sorting").get()

        self.home_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.home_frame.pack(side=tk.LEFT)
        self.home_frame.pack_propagate(False)
        self.home_frame.configure(width=self.root.winfo_screenwidth() - 150, height=self.root.winfo_screenheight())

        logo_path = "/home/pi/Downloads/ui/sort_logo.png"
        self.show_logo(logo_path, self.home_frame, 250, 30)

        logo_path = "/home/pi/Downloads/ui/tomato_sorting.png"
        self.show_logo(logo_path, self.home_frame, 200, 20)

        # Create a frame to hold the two boxes
        self.boxes_frame = tk.Frame(self.home_frame, bg="#FFFFFF")
        self.boxes_frame.pack(fill=tk.BOTH, expand=True)

        # Create the left box
        self.left_box = tk.Frame(self.boxes_frame, bg="#97d0c4", bd=2, highlightbackground="#286c6e",
                                 highlightthickness=2)
        self.left_box.grid(row=0, column=0, sticky="nsew", padx=5, pady=3)
        self.boxes_frame.grid_columnconfigure(0, weight=2)  # Set weight of column 0
        self.boxes_frame.grid_rowconfigure(0, weight=1)


        # Add content to the left box
        self.left_label = tk.Label(self.left_box, text="LIVE FEED", font=('Orbitron', 10), bg="#97d0c4")
        self.left_label.pack(padx=20, pady=3, anchor="nw")

        self.live_feed_label = tk.Frame(self.left_box, bg="#FFFFFF", highlightbackground="#22a0f5", highlightthickness=2)
        self.live_feed_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)

        logo_path = "/home/pi/Downloads/ui/initials_logo.jpg"
        logo = Image.open(logo_path)

        # Get the size of the live_feed_label
        live_feed_label_width = 150
        live_feed_label_height = 80

        # Resize the logo to fit the live_feed_label
        logo = logo.resize((live_feed_label_width, live_feed_label_height), Image.LANCZOS)

        photo_image = ImageTk.PhotoImage(logo)
        self.photo_label = tk.Label(self.live_feed_label, image=photo_image, bg="white")
        self.photo_label.image = photo_image
        self.photo_label.pack(pady=3, fill=tk.BOTH, expand=True)  # Fill both horizontally and vertically

        # Create a small box with background #fbc9cc
        self.live_feed_result_box = tk.Frame(self.left_box, bg="#fbc9cc", width=50, height=50)
        self.live_feed_result_box.pack(fill=tk.BOTH, padx=50, pady=10)


        self.live_feed_result = tk.Label(self.live_feed_result_box, text="TOMATO CLASSIFICATION: ", font=('Orbitron', 10), bg="#fbc9cc",
                                      justify="center")
        self.live_feed_result.grid(row=2, column=1, padx=(20, 20), pady=3, sticky="e")


        # Create the right box
        self.right_box = tk.Frame(self.boxes_frame, bg="#fbc9cc", bd=2, highlightbackground="#b5141f",
                                  highlightthickness=2)
        self.right_box.grid(row=0, column=1, sticky="nsew", padx=5, pady=3)
        self.boxes_frame.grid_columnconfigure(1, weight=1)  # Set weight of column 1

        # Add content to the right box
        right_label = tk.Label(self.right_box, text="TOMATO COUNTER", font=('Orbitron', 10), bg="#fbc9cc")
        right_label.pack(padx=20, pady=3)

        self.unripe_count_box = tk.Frame(self.right_box, bg="#FFFFFF", highlightbackground="#fbc9cc", highlightthickness=2)
        self.unripe_count_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=1)

        self.turning_count_box = tk.Frame(self.right_box, bg="#FFFFFF", highlightbackground="#fbc9cc", highlightthickness=2)
        self.turning_count_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=1)

        self.ripe_count_box = tk.Frame(self.right_box, bg="#FFFFFF", highlightbackground="#fbc9cc", highlightthickness=2)
        self.ripe_count_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=1)

        # Create a label for the unripe count
        unripe_label = tk.Label(self.unripe_count_box, text="UNRIPE", font=('Orbitron', 10), bg="#FFFFFF", justify="center")
        unripe_label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky="w")

        self.unripe_count_label = tk.Label(self.unripe_count_box, text="0", font=('Orbitron', 30), bg="#FFFFFF",
                                      justify="center")
        self.unripe_count_label.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="e")

        # Create a label for the turning count
        turning_label = tk.Label(self.turning_count_box, text="TURNING", font=('Orbitron', 10), bg="#FFFFFF",
                                 justify="center")
        turning_label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky="w")

        self.turning_count_label = tk.Label(self.turning_count_box, text="0", font=('Orbitron', 30), bg="#FFFFFF",
                                       justify="center")
        self.turning_count_label.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="e")

        # Create a label for the ripe count
        ripe_label = tk.Label(self.ripe_count_box, text="RIPE", font=('Orbitron', 10), bg="#FFFFFF", justify="center")
        ripe_label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky="w")

        self.ripe_count_label = tk.Label(self.ripe_count_box, text="0", font=('Orbitron', 30), bg="#FFFFFF", justify="center")
        self.ripe_count_label.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="e")

        self.sort_count_total_label = tk.Label(self.right_box, text="TOTAL: 0", font=('Orbitron', 15), bg="#97d0c4", justify="center")
        self.sort_count_total_label.pack(fill=tk.BOTH, padx=50, pady=3)

        # Load the image
        original_image = Image.open("/home/pi/Downloads/ui/sort_start_button.png")

        # Resize the image to fit within the button
        width, height = original_image.size
        max_width = 130
        max_height = 25

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = original_image

        # Convert the resized image to a PhotoImage
        image = ImageTk.PhotoImage(resized_image)

        # Create the button with the image
        self.sort_start_btn  = tk.Button(self.left_box, image=image, bd=0, borderwidth=0)
        
        if sorting.val() == 0:
            self.sort_start_btn.pack(pady=3)
        self.sort_start_btn.image = image
        
        self.sort_start_btn.bind("<Button-1>", self.start_sorting_callback)
        
        # Load the image
        original_image = Image.open("/home/pi/Downloads/ui/sort_stop_button.png")

        # Resize the image to fit within the button
        width, height = original_image.size
        max_width = 130
        max_height = 25

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = original_image

        # Convert the resized image to a PhotoImage
        image = ImageTk.PhotoImage(resized_image)

        # Create the button with the image
        self.sort_stop_btn  = tk.Button(self.left_box, image=image, bd=0, borderwidth=0)

        if sorting.val() == 1:
            self.sort_stop_btn.pack(pady=3)
        self.sort_stop_btn.image = image
        
        self.sort_stop_btn.bind("<Button-1>", self.stop_sorting_callback)
        
        update_ui = True

    def show_kool_page(self):
        global current_menu, update_ui
        current_menu = 2
        update_ui = False
        self.clear_main_frame()
        
        
        preservation = db.child("sorter").child("operation").child("operate").child("preservation").get()
        
        
        self.home_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.home_frame.pack(side=tk.LEFT)
        self.home_frame.pack_propagate(False)
        self.home_frame.configure(width=self.root.winfo_screenwidth() - 114, height=self.root.winfo_screenheight())

        logo_path = "/home/pi/Downloads/ui/sort_logo.png"
        self.show_logo(logo_path, self.home_frame, 250, 30)

        logo_path = "/home/pi/Downloads/ui/tomato_preservation.png"
        self.show_logo(logo_path, self.home_frame, 250, 20)

        # Create a frame to hold the two boxes
        self.boxes_frame = tk.Frame(self.home_frame, bg="#FFFFFF")
        self.boxes_frame.pack(fill=tk.BOTH, expand=True)

        # Create the left box
        self.left_box = tk.Frame(self.boxes_frame, bg="#97d0c4", bd=2, highlightbackground="#286c6e",
                                 highlightthickness=2)
        self.left_box.grid(row=0, column=0, sticky="nsew", padx=5, pady=3)
        self.boxes_frame.grid_columnconfigure(0, weight=2)  # Set weight of column 0
        self.boxes_frame.grid_rowconfigure(0, weight=1)

        # Add content to the left box
        self.left_label = tk.Label(self.left_box, text="TEMPERATURE", font=('Orbitron', 10), bg="#97d0c4")
        self.left_label.pack(padx=20, pady=3, anchor="nw")

        self.live_sensor_label = tk.Frame(self.left_box, bg="#97d0c4")
        self.live_sensor_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=(3, 0))

        # Create the frame for sensor titles
        self.live_sensor_title_label = tk.Frame(self.left_box, bg="#97d0c4")
        self.live_sensor_title_label.pack(padx=10, pady=3)

        # Create sensor boxes inside the live sensor label frame
        sensor_box1 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box1.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        sensor_box2 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box2.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        sensor_box3 = tk.Frame(self.live_sensor_label, bg="#FFFFFF", bd=2, highlightbackground="#22a0f5",
                               highlightthickness=2)
        sensor_box3.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Create sensor title labels inside the live sensor title label frame
        sensor_title1 = tk.Label(self.live_sensor_title_label, text="Unripe", font=('Orbitron', 12), bg="#97d0c4")
        sensor_title1.pack(side=tk.LEFT, padx=10, pady=3)

        sensor_title2 = tk.Label(self.live_sensor_title_label, text="Turning", font=('Orbitron', 12), bg="#97d0c4")
        sensor_title2.pack(side=tk.LEFT, padx=10, pady=3)

        sensor_title3 = tk.Label(self.live_sensor_title_label, text="Ripe", font=('Orbitron', 12), bg="#97d0c4")
        sensor_title3.pack(side=tk.LEFT, padx=10, pady=3)

        self.sensor_data_label1 = tk.Label(sensor_box1, text="0°C", font=('Orbitron', 15), bg="#FFFFFF",
                                      justify="center")
        self.sensor_data_label1.pack(expand=True, fill=tk.BOTH)

        self.sensor_data_label2 = tk.Label(sensor_box2, text="0°C", font=('Orbitron', 15), bg="#FFFFFF",
                                      justify="center")
        self.sensor_data_label2.pack(expand=True, fill=tk.BOTH)

        self.sensor_data_label3 = tk.Label(sensor_box3, text="0°C", font=('Orbitron', 15), bg="#FFFFFF",
                                      justify="center")
        self.sensor_data_label3.pack(expand=True, fill=tk.BOTH)

        # Create a small box with background #fbc9cc
        self.live_feed_result_box = tk.Frame(self.left_box, bg="#fbc9cc", width=50, height=50)
        self.live_feed_result_box.pack(fill=tk.BOTH, padx=50, pady=3)

        self.live_sensor_result = tk.Label(self.live_feed_result_box, text="TIME RUNNING: ", font=('Orbitron', 10),
                                    bg="#fbc9cc",
                                    justify="center")
        self.live_sensor_result.grid(row=2, column=1, padx=(20, 20), pady=5, sticky="e")

        # Create the right box
        self.right_box = tk.Frame(self.boxes_frame, bg="#fbc9cc", bd=2, highlightbackground="#b5141f",
                                  highlightthickness=2)
        self.right_box.grid(row=0, column=1, sticky="nsew", padx=5, pady=3)
        self.boxes_frame.grid_columnconfigure(1, weight=1)  # Set weight of column 1

        # Add content to the right box
        right_label = tk.Label(self.right_box, text="COOLING GUIDE", font=('Orbitron', 10), bg="#fbc9cc")
        right_label.pack(padx=20, pady=3)

        cooling_guide_label = tk.Frame(self.right_box, bg="#FFFFFF", highlightbackground="#fbc9cc", highlightthickness=2)
        cooling_guide_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)

        # Load the image
        original_image = Image.open("/home/pi/Downloads/ui/sort_start_button.png")

        # Resize the image to fit within the button
        width, height = original_image.size
        max_width = 130
        max_height = 25

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = original_image

        # Convert the resized image to a PhotoImage
        image = ImageTk.PhotoImage(resized_image)

        # Create the button with the image
        self.preserve_start_btn = tk.Button(self.left_box, image=image, bd=0, borderwidth=0)
        if preservation.val() == 0:
            self.preserve_start_btn.pack(pady=3)
        self.preserve_start_btn.image = image
        
        self.preserve_start_btn.bind("<Button-1>", self.start_preservation_callback)
        
        # Load the image
        original_image = Image.open("/home/pi/Downloads/ui/sort_stop_button.png")

        # Resize the image to fit within the button
        width, height = original_image.size
        max_width = 130
        max_height = 25

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = original_image

        # Convert the resized image to a PhotoImage
        image = ImageTk.PhotoImage(resized_image)

        # Create the button with the image
        self.preserve_stop_btn  = tk.Button(self.left_box, image=image, bd=0, borderwidth=0)
        if preservation.val() == 1:
            self.preserve_stop_btn.pack(pady=3)
        self.preserve_stop_btn.image = image
        
        self.preserve_stop_btn.bind("<Button-1>", self.stop_preservation_callback)
        
        update_ui = True

    def clear_main_frame(self):
        # Function to clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()



    def start_sorting_callback(self, event):
        global update_ui
        update_ui = True
        # Define actions to be performed when the "Start Sorting" button is clicked
        print("Start Sorting button clicked")
        self.sort_start_btn.pack_forget()
        self.sort_stop_btn.pack(pady=3)
        operate_to_save = {
            "sorting": 1,
        }
        db.child("sorter").child("operation").child("operate").update(operate_to_save)
        
        self.start_database_update_thread()
        self.start_database_update_thread2()
        #self.start_timer_thread()
        
       
        

    def start_preservation_callback(self, event):
        global update_ui
        global seconds
        seconds = 0
        update_ui = True
        # Define actions to be performed when the "Start Preservation" button is clicked
        print("Start Preservation button clicked")
        self.preserve_start_btn.pack_forget()
        self.preserve_stop_btn.pack(pady=3)
        operate_to_save = {
            "preservation": 1,
        }
        db.child("sorter").child("operation").child("operate").update(operate_to_save)
        
        self.start_database_update_thread()
        self.start_database_update_thread2()
        self.start_timer_thread()
        
        

    def stop_sorting_callback(self, event):
        global update_ui
        update_ui = False
        # Define actions to be performed when the "Start Sorting" button is clicked
        print("Stop Sorting button clicked")
        self.sort_start_btn.pack(pady=3)
        self.sort_stop_btn.pack_forget()
        operate_to_save = {
            "sorting": 0,
        }
        db.child("sorter").child("operation").child("operate").update(operate_to_save)
        
       

    def stop_preservation_callback(self, event):
        
        global update_ui
        update_ui = False
        # Define actions to be performed when the "Start Preservation" button is clicked
        print("Stop Preservation button clicked")
        self.preserve_start_btn.pack(pady=3)
        self.preserve_stop_btn.pack_forget()
        operate_to_save = {
            "preservation": 0,
        }
        db.child("sorter").child("operation").child("operate").update(operate_to_save)
        
       
    
    def print_timer(self):
        global seconds
        global update_ui  
        global current_menu
        
        seconds = 0
        time.sleep(3)
        while True:
            if update_ui == True:
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds_remainder = seconds % 60
                
                if current_menu == 2:
                    if hasattr(self, 'live_sensor_result') and self.live_sensor_result:
                        self.live_sensor_result.config(text=f"TIME RUNNING: {hours:02d}H {minutes:02d}M {seconds_remainder:02d}S")
                elif current_menu == 0:
                    if hasattr(self, 'home_timer_label') and self.home_timer_label:
                        self.home_timer_label.config(text=f"TIME RUNNING: {hours:02d}H {minutes:02d}M {seconds_remainder:02d}S")
                    
                seconds += 1
                
            time.sleep(1)
            
            
    def update_labels_from_database(self):
        global update_ui
        global temperature1, temperature2, temperature3, humidity1, humidity2, humidity3
        global unripe_count, turning_count, ripe_count
        global tomato_classification
        tomato_classification = ""
        
        
        unripe_count = 0
        turning_count = 0
        ripe_count = 0

        while True:
            if current_menu == 0 and update_ui == True:
                datas = db.child("sorter").child("datas").get()
            
                for data in datas.each():
                    print(data)
                    if data.key() == "unripe":
                    
                        unripe_count = data.val()
                    
                        self.sensor_data_label11.config(text=unripe_count)
                    elif data.key() == "turning":
                    
                        turning_count = data.val()
                        self.sensor_data_label22.config(text=turning_count)
                    
                    elif data.key() == "ripe":
                        ripe_count = data.val()
                        self.sensor_data_label33.config(text=ripe_count)
                        
                total = unripe_count + turning_count + ripe_count
                self.home_total.config(text="TOTAL: " + str(total))
                        
                datas = db.child("sorter").child("temperatures").get()
            
                for data in datas.each():
                    if data.key() == "temperature1":
                    
                        temperature1 = data.val()
                    
                        self.sensor_data_label111.config(text=str(temperature1) + "°C")
                    elif data.key() == "temperature2":
                    
                        temperature2 = data.val()
                        self.sensor_data_label222.config(text=str(temperature2) + "°C")
                    
                    elif data.key() == "temperature3":
                        temperature3 = data.val()
                        self.sensor_data_label333.config(text=str(temperature3) + "°C")
                
                time.sleep(3)
                
            
            elif current_menu == 1 and update_ui == True:
                #print("Detecting")
                detection = db.child("sorter").child("device").child("detection").get()

                frame_as_base64 = detection.val()
                image_data = base64.b64decode(frame_as_base64)
                photo_image = ImageTk.PhotoImage(Image.open(io.BytesIO(image_data)).resize((380, 200), Image.LANCZOS))
            
                self.photo_label.config(image=photo_image)
                self.photo_label.image = photo_image
                self.photo_label.config(width=photo_image.width(), height=photo_image.height())
                time.sleep(0.5)
            
            elif current_menu == 2 and update_ui == True:
                datas = db.child("sorter").child("temperatures").get()
                
                for data in datas.each():
                    
                    if data.key() == "temperature1":
                    
                        temperature1 = data.val()
                    
                        self.sensor_data_label1.config(text=str(temperature1) + "°C")
                    elif data.key() == "temperature2":
                    
                        temperature2 = data.val()
                        self.sensor_data_label2.config(text=str(temperature2) + "°C")
                    
                    elif data.key() == "temperature3":
                        temperature3 = data.val()
                        self.sensor_data_label3.config(text=str(temperature3) + "°C")
                
                time.sleep(5)
                
    def update_labels_from_database2(self):
        global update_ui
        global unripe_count, turning_count, ripe_count
        
        unripe_count = 0
        turning_count = 0
        ripe_count = 0

        while True:
            if current_menu == 1 and update_ui == True:
            
                datas = db.child("sorter").child("datas").get()
            
                for data in datas.each():
                    
                    if data.key() == "unripe":
                    
                        unripe_count = data.val()
                    
                        self.unripe_count_label.config(text=unripe_count)
                    elif data.key() == "turning":
                    
                        turning_count = data.val()
                        self.turning_count_label.config(text=turning_count)
                    
                    elif data.key() == "ripe":
                        ripe_count = data.val()
                        self.ripe_count_label.config(text=ripe_count)
                    elif data.key() == "detection":
                        self.live_feed_result.config(text="TOMATO CLASSIFICATION: " + data.val())
        
                total = unripe_count + turning_count + ripe_count
                
                self.sort_count_total_label.config(text="TOTAL: " + str(total))
                   
                time.sleep(3)
            
            

    def start_database_update_thread(self):
        # Create and start the thread
        update_thread = threading.Thread(target=self.update_labels_from_database)
        update_thread.daemon = True  # Daemonize the thread to stop it when the main program exits
        update_thread.start()
        
    def start_database_update_thread2(self):
        # Create and start the thread
        update_thread2 = threading.Thread(target=self.update_labels_from_database2)
        update_thread2.daemon = True  # Daemonize the thread to stop it when the main program exits
        update_thread2.start()
        
    def start_timer_thread(self):
        # Create and start the thread
        timer_thread = threading.Thread(target=self.print_timer)
        timer_thread.daemon = True  # Daemonize the thread to stop it when the main program exits
        timer_thread.start()

root = tk.Tk()
# root.attributes('-fullscreen', True)
root.attributes('-zoomed', True)
#root.geometry("800x400")
app = RPiApp(root)
app.indicate2()
#app.start_database_update_thread()

root.mainloop()

