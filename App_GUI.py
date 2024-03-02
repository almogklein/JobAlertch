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

        # Load the logo image and configure the layout
        self.load_and_display_logo('src/UntitledR.png')  # Change path as necessary

        # UI Elements Initialization
        self.initialize_ui_elements()

        # Log Display Initialization
        self.initialize_log_display()

        # Additional UI for data visualization
        self.enlarge_button = Button(self.m_root_control, text="Enlarge & Visualize",
                                     command=self.enlarge_and_visualize)
        self.enlarge_button.pack(side=tk.TOP, padx=5, pady=5)

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
        self.m_root_control.geometry("1200x800")  # Adjust size as needed

        # Create a frame for the figures if it doesn't exist
        if not self.figures_frame:
            self.figures_frame = Frame(self.m_root_control)
            self.figures_frame.pack(fill=tk.BOTH, expand=True)

        # Display statistics and graphs
        self.display_statistics()
        self.display_graphs()

    def display_statistics(self):
        """
        Displays total records and daily submissions.
        """
        if (not self.dataframe.empty):
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
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        ax1.bar(['Sample1', 'Sample2'], [10, 3])  # Replace with actual data
        canvas1 = FigureCanvasTkAgg(fig1, master=self.figures_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # fig2, ax2 = plt.subplots(figsize=(5, 4))
        # ax2.scatter(np.random.rand(10), np.random.rand(10))  # Replace with actual data
        # canvas2 = FigureCanvasTkAgg(fig2, master=self.figures_frame)
        # canvas2.draw()
        # canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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

        # # Remove Button
        # self.remove_button = Button(self.m_root_control, text="Remove Document", command=self.remove_document)
        # self.remove_button.pack(side=tk.TOP, padx=5, pady=5)

        # Quit Button
        self.quit_button = Button(self.m_root_control, text="Quit", command=self.quit_application)
        self.quit_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def initialize_log_display(self):
        """
        Initializes the log display area.
        """
        self.log_display = scrolledtext.ScrolledText(self.m_root_control, height=3, state='disabled')
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
        self.log_message(f"file loaded: {file_path}")
        self.dataframe = pd.read_csv(file_path)
        self.dataframe = self.dataframe[['Job ID', 'Date of Submission', 'Company Name', 'Position',
                                         'Job Location', 'Job URL', 'Application Method', 'Resume Version',
                                         'Job Status', 'Interview Dates', 'Feedback', 'Notes']]
        self.dataframe = self.dataframe.dropna(axis=0, how='all')

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
                # Example: Extract job name, company name, and location from the HTML
                # Update these selectors based on the actual HTML structure of your target job posting sites
                job_text = soup.find('head').text.strip()

                job_name = job_text.split("hiring")[1].split(" in ")[0][1:]
                company_name = job_text.split("hiring")[0][:-1]
                location = job_text.split("hiring")[1].split(" in ")[1].split("|")[0][:-1]

                self.append_to_csv(self.m_aUploadedFiles[0], [job_name, company_name, location, url, ('Easy Apply' if self.apply_switch.get() == 0 else 'Carer')])
            else:
                self.log_message(f"Failed to fetch URL, response: {response.status_code}")

        except Exception as e:
            self.log_message(f"Failed to fetch or parse URL: {e}")
            print(f"Failed to fetch or parse URL: {e}")

    def append_to_csv(self, file_path, data):

        self.dataframe = self.dataframe.append({'Job ID': self.dataframe.shape[0] + 1,
                                                'Date of submisstion': datetime.now().strftime("%Y-%m-%d"),
                                                'Company Name': data[1],
                                                'Position': data[0],
                                                'Job Location': data[2],
                                                'Job URL': data[3],
                                                'Application Method': data[4]},
                                               ignore_index=True)
        self.dataframe = self.dataframe.fillna('-')
        self.dataframe.to_csv(file_path)
        self.dataframe = pd.read_csv(file_path)

        if 'Unnamed: 0' in self.dataframe.columns:
            self.dataframe.pop('Unnamed: 0')

        self.dataframe = self.dataframe.dropna(axis=0, how='all')

        self.log_message(f"Data added to file: {data}")
        print("Data added to file:", data)

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

if __name__ == "__main__":
    control_app = ControlWindow(tk.Tk())

