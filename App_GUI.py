import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import scrolledtext, Canvas, Label, Button, Toplevel, Frame, OptionMenu, StringVar, Entry
import requests
from bs4 import BeautifulSoup
import csv
import os
import numpy as np
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QFileDialog, QTextEdit, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ControlWindow:
    """
    Class representing the main control window of the application.
    """
    def __init__(self, a_root):
        """
        Constructor for ControlWindow.

        Parameters:
        - a_root (Tk): The main Tkinter root window.
        """

        self.m_root_control = a_root
        self.m_root_control.title("JobAlertch - Control Window")
        self.m_aUploadedFiles = []

        self.m_root_control.iconbitmap('src/1_7We_icon.ico')

        logo_image = Image.open('src/1_7We_icon.ico')
        photo = ImageTk.PhotoImage(logo_image)
        self.m_root_control.tk.call('wm', 'iconphoto', self.m_root_control._w, photo)

        # Load the logo image and configure the layout
        self.load_and_display_logo('src/UntitledR.png')  # Change path as necessary

        # UI Elements Initialization
        self.initialize_ui_elements()

        # Log Display Initialization
        self.initialize_log_display()

        # Attributes for data visualization
        self.figures_frame = None  # Will hold the matplotlib figures
        self.dataframe = None

        # Main loop
        self.m_root_control.mainloop()

    def enlarge_and_visualize(self):
        """
        Enlarges the window and displays data visualizations.
        """
        # Enlarge the window
        # self.m_root_control.geometry("1200x800")  # Adjust size as needed

        # Create a frame for the figures if it doesn't exist
        # if not self.figures_frame:
        self.figures_frame = Frame(self.m_root_control)
        self.figures_frame.pack(fill=tk.BOTH, expand=True)
        # Display statistics and graphs
        self.display_statistics()
        self.display_graphs()



    def display_statistics(self):
        """
        Displays total records and daily submissions.
        """
        # if (not self.dataframe.empty):
        total_records = len(self.dataframe)
        today = datetime.now().strftime("%Y-%m-%d")
        daily_submissions = len(self.dataframe[self.dataframe['Date of Submission'] == today])

        # Update or create labels for displaying the statistics
        total_label_text = f"Total Records: {total_records}"
        daily_label_text = f"Today's Submissions: {daily_submissions}"

        total_label = Label(self.figures_frame, text=total_label_text)
        total_label.pack(side=tk.LEFT, padx=5, pady=5)

        daily_label = Label(self.figures_frame, text=daily_label_text)
        daily_label.pack(side=tk.LEFT, padx=5, pady=5)

    def display_graphs(self):
        """
        Displays bar and scatter graphs based on the data.
        """
        # Placeholder data and plots - replace with your actual data and plotting logic
        total_records = len(self.dataframe)
        today = datetime.now().strftime("%Y-%m-%d")
        daily_submissions = len(self.dataframe[self.dataframe['Date of Submission'] == today])

        # Bar graph for total records and daily submissions
        labels = ['Total Records', 'Daily Submissions']
        values = [total_records, daily_submissions]
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        bars = ax1.bar(labels, values)  # Create the bars

        # Add the numerical values above each bar
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, height,
                     f'{int(height)}',  # Convert to int for display, or use '{:.2f}'.format(height) for decimal values
                     ha='center', va='bottom')

        canvas1 = FigureCanvasTkAgg(fig1, master=self.figures_frame)  # Embed the plot in the Tkinter widget
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def load_and_display_logo(self, image_path):
        """
        Loads and displays the logo image.
        """
        try:
            logo_image = Image.open(image_path)
            logo_image = logo_image.resize((200, 200), Image.ANTIALIAS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = Label(self.m_root_control, image=logo_photo)
            self.logo_label.image = logo_photo  # Keep a reference.
            self.logo_label.pack(padx=10, pady=5)
        except Exception as e:
            print(f"Error loading logo image: {e}")

    def initialize_ui_elements(self):
        """
        Initializes and packs UI elements.
        """
        # URL Entry
        self.url_entry_label = Label(self.m_root_control, text="Enter Job URL:")
        self.url_entry_label.pack(side=tk.TOP, padx=5, pady=5)
        self.url_entry = Entry(self.m_root_control, width=30)
        self.url_entry.pack(side=tk.TOP, padx=5, pady=5)

        # # Label for the switch
        self.apply_label = tk.Label(self.m_root_control, text="Toggle for EazyApply or Career:")
        self.apply_switch = tk.Scale(self.m_root_control, from_=0, to=1, orient=tk.HORIZONTAL, length=100,
                                     showvalue=0, sliderlength=25, tickinterval=1, resolution=1,
                                     command=self.update_label)
        # Initial position of the switch
        self.apply_switch.set(0)  # Set to 0 for EazyApply, 1 for Career
        self.current_choice_label = tk.Label(self.m_root_control, text="EazyApply")
        self.apply_label.pack(side=tk.TOP, padx=5, pady=5)
        self.apply_switch.pack(side=tk.TOP, padx=5, pady=5)
        self.current_choice_label.pack(side=tk.TOP, padx=5, pady=5)


        # Fetch Button
        self.fetch_button = Button(self.m_root_control, text="Fetch and Add", command=self.fetch_from_url)
        self.fetch_button.pack(side=tk.TOP, padx=5, pady=5)

        # Browse Button
        self.browse_button = Button(self.m_root_control, text="Browse", command=self.browse_files)
        self.browse_button.pack(side=tk.TOP, padx=5, pady=5)

        # Additional UI for data visualization
        self.enlarge_button = Button(self.m_root_control, text="Enlarge & Visualize", command=self.enlarge_and_visualize)
        self.enlarge_button.pack(side=tk.TOP, padx=5, pady=5)

        # Quit Button
        self.quit_button = Button(self.m_root_control, text="Quit", command=self.quit_application)
        self.quit_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def initialize_log_display(self):
        """
        Initializes the log display area.
        """
        self.log_display = scrolledtext.ScrolledText(self.m_root_control, height=5, state='disabled')
        self.log_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def log_message(self, message):
        """
        Logs a message to the scrolled text area.
        """
        self.log_display.config(state='normal')
        self.log_display.insert(tk.END, message + '\n')
        self.log_display.config(state='disabled')
        # Automatically scroll to the bottom
        self.log_display.yview(tk.END)

    def browse_files(self):

        filetypes = [("CSV Files", "*.csv")]
        files = filedialog.askopenfilename(defaultextension=".csv", filetypes=filetypes)
        self.m_aUploadedFiles.append(files)
        # self.pack_self()

        file_path = self.m_aUploadedFiles[0]  # original_file_name = os.path.basename(file_path)

        self.dataframe = pd.read_csv(file_path)
        self.dataframe = self.dataframe[['Job ID', 'Date of Submission', 'Company Name', 'Position',
                                         'Job Location', 'Job URL', 'Application Method', 'Resume Version',
                                         'Job Status', 'Interview Dates', 'Feedback', 'Notes']]
        self.dataframe = self.dataframe.dropna(axis=0, how='all')
        self.log_message(f"file loaded: {file_path}")

    def fetch_from_url(self):
        url = self.url_entry.get()
        if not url:
            self.log_message("URL is empty")
            print("URL is empty")
            return

        try:
            response = requests.get(url)
            if (response.status_code == 200):
                soup = BeautifulSoup(response.content, 'html.parser')

                # response.content.decode()
                job_text = soup.find('head').text.strip()

                job_name = job_text.split("hiring")[1].split(" in ")[0][1:]
                company_name = job_text.split("hiring")[0][:-1]
                location = job_text.split("hiring")[1].split(" in ")[1].split("|")[0][:-1]

                self.append_to_csv(self.m_aUploadedFiles[0], [job_name, company_name, location, url, ('Easy Apply' if self.apply_switch.get() == 0 else 'Carer')])

            if (response.status_code == 429):

                times = 15
                while (times):
                    response = requests.get(url)
                    if (response.status_code == 200):
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # response.content.decode()
                        job_text = soup.find('head').text.strip()

                        job_name = job_text.split("hiring")[1].split(" in ")[0][1:]
                        company_name = job_text.split("hiring")[0][:-1]
                        location = job_text.split("hiring")[1].split(" in ")[1].split("|")[0][:-1]

                        self.append_to_csv(self.m_aUploadedFiles[0], [job_name, company_name, location, url, (
                            'Easy Apply' if self.apply_switch.get() == 0 else 'Carer')])
                        break
                    times-=1

                if (response.status_code != 200):
                    #     self.log_message(f"Failed to fetch URL {16 - times} times!")
                    # else:
                    self.log_message(f"Failed to fetch URL 15 times! {response.status_code}")

        except Exception as e:
            self.log_message(f"Failed to fetch or parse URL: {e}")
            print(f"Failed to fetch or parse URL: {e}")

    def append_to_csv(self, file_path, data):

        if (self.dataframe[(self.dataframe['Company Name'] == data[1]) & (self.dataframe['Position'] == data[0])].empty):
            new_row = pd.DataFrame({
                'Job ID': [self.dataframe.shape[0] + 1],
                'Date of Submission': [datetime.now().strftime("%Y-%m-%d")],
                'Company Name': [data[1]],
                'Position': [data[0]],
                'Job Location': [data[2]],
                'Job URL': [data[3]],
                'Application Method': [data[4]]
            })
            self.dataframe = pd.concat([self.dataframe, new_row], ignore_index=True)

            self.dataframe = self.dataframe.fillna('-')
            self.dataframe.to_csv(file_path)
            self.dataframe = pd.read_csv(file_path)

            if 'Unnamed: 0' in self.dataframe.columns:
                self.dataframe.pop('Unnamed: 0')

            self.dataframe = self.dataframe.dropna(axis=0, how='all')

            self.log_message(f"Data added to file: {data}\n\n")
            print("Data added to file:", data)
        else:
            self.log_message(f"job alredy in sheet: {self.dataframe[(self.dataframe['Company Name'] == data[1]) & (self.dataframe['Position'] == data[0])]['Date of Submission']} {data}\n\n")
            print("job alredy in sheet: ", data)

    def update_label(self, event):
        if self.apply_switch.get() == 0:
            self.current_choice_label.config(text="EazyApply")
        else:
            self.current_choice_label.config(text="Career")

    def quit_application(self):
        """
        Quit the application.
        """
        self.m_root_control.quit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('JobAlertch - Control Window')
        self.setWindowIcon(QIcon('src/1_7We_icon.ico'))
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.logo_label = QLabel(self)
        pixmap = QPixmap('src/UntitledR.png')
        self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)  # Centering the logo
        self.layout.addWidget(self.logo_label)

        self.dataframe = pd.DataFrame(columns=['Job ID', 'Date of Submission', 'Company Name', 'Position', 'Job Location', 'Job URL', 'Application Method'])

        self.setup_ui()
        self.figures_frame = QHBoxLayout()
        self.layout.addLayout(self.figures_frame)

        self.figure = plt.figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        self.figures_frame.addWidget(self.canvas)

    def setup_ui(self):
        self.url_entry = QLineEdit(self)
        self.url_entry.setPlaceholderText("Enter Job URL:")
        self.fetch_button = QPushButton('Fetch and Add', self)
        self.fetch_button.clicked.connect(self.fetch_from_url)
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_files)
        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.url_entry)
        self.layout.addWidget(self.fetch_button)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.quit_button)
        self.log_display = QTextEdit(self)
        self.log_display.setReadOnly(True)
        self.layout.addWidget(self.log_display)

    def fetch_from_url(self):
        url = self.url_entry.text()
        if not url:
            self.log_message("URL is empty")
            return

        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_text = soup.find('head').text.strip()
                job_name = job_text.split("hiring")[1].split(" in ")[0][1:]
                company_name = job_text.split("hiring")[0][:-1]
                location = job_text.split("hiring")[1].split(" in ")[1].split("|")[0][:-1]
                self.append_to_dataframe([job_name, company_name, location, url, 'Easy Apply'])
            elif response.status_code == 429:
                self.log_message("Too many requests. Please try again later.")
            else:
                self.log_message(f"Failed to fetch URL: {response.status_code}")
        except Exception as e:
            self.log_message(f"Error: {e}")

    def append_to_dataframe(self, data):
        if not ((self.dataframe['Company Name'] == data[1]) & (self.dataframe['Position'] == data[0])).any():
            new_row = pd.DataFrame([{
                'Job ID': len(self.dataframe) + 1,
                'Date of Submission': datetime.now().strftime("%Y-%m-%d"),
                'Company Name': data[1],
                'Position': data[0],
                'Job Location': data[2],
                'Job URL': data[3],
                'Application Method': data[4]
            }])
            self.dataframe = pd.concat([self.dataframe, new_row], ignore_index=True)
            self.dataframe.to_csv(self.data_path, index=False)
            self.log_message(f"Data added: {data}")
            self.update_graph()
        else:
            self.log_message(f"Job already in sheet: {data}")

    def browse_files(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open CSV file", "", "CSV Files (*.csv)")
        if fname:
            self.dataframe = pd.read_csv(fname)
            self.log_message(f"File loaded: {fname}")
            self.data_path = fname
            self.update_graph()

    def update_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if not self.dataframe.empty:
            total_records = len(self.dataframe)
            today = datetime.now().strftime("%Y-%m-%d")
            daily_submissions = self.dataframe[self.dataframe['Date of Submission'] == today].count()[
                'Date of Submission']
            labels = ['Total Records', 'Daily Submissions']
            values = [total_records, daily_submissions]
            bars = ax.bar(labels, values)
            ax.set_ylim(0, max(values) * 1.2)  # Increase the y-limit to 120% of the highest bar value
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')
            ax.set_title('Job Submissions Overview')
        self.canvas.draw()

    def log_message(self, message):
        self.log_display.append(message)