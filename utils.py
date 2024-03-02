import tkinter as tk

class CUtillistion:

    # Function to update LED colors
    def update_led_based_on_trigger(self, canvas, trigger_value):
        if trigger_value == 1:
            self.update_led_colors(canvas, 'green')
        elif trigger_value == -1:
            self.update_led_colors(canvas, 'red')
        elif trigger_value == 0:
            self.update_led_colors(canvas, 'white')
        
    def update_led_colors(self, a_oled_can, color):
        """
        Update the colors of the LED circles.

        Parameters:
        - colors (list): A list of color names for each LED circle.
        """
        a_oled_can.itemconfig(1, fill=color)

    def process_movement(self, data_status_logs_display, mean_value, mean_value1, mean_value2, threshold, canvas, start_message, positive_color='green', negative_color='red', no_movement_color='white', SLOPE_THRESHOLD_HIGH=3):
        if mean_value > threshold and (mean_value > SLOPE_THRESHOLD_HIGH * mean_value1 or mean_value > SLOPE_THRESHOLD_HIGH * mean_value2):
            self.set_port_message(f'{start_message} at Slop {mean_value:.2f}', data_status_logs_display)
            print(f'\n{start_message} at Slop {mean_value:.2f}')
            self.update_led_colors(canvas, positive_color)
            return 1
        elif mean_value < -threshold and (mean_value < -SLOPE_THRESHOLD_HIGH * mean_value1 or mean_value < -SLOPE_THRESHOLD_HIGH * mean_value2):
            self.set_port_message(f'End {start_message} at Slop {mean_value:.2f}', data_status_logs_display)
            print(f'\nEnd {start_message} at Slop {mean_value:.2f}')
            self.update_led_colors(canvas, negative_color)
            return -1
        else:
            self.update_led_colors(canvas, no_movement_color)
            return 0
    
    def set_port_message(self, a_smessage, data_port_display):
        """
        Set a message in the display.

        Parameters:
        - a_smessage (str): The message to be displayed.
        """
        data_port_display.config(state=tk.NORMAL)
        data_port_display.insert(tk.END, a_smessage + "\n")
        data_port_display.config(state=tk.DISABLED)