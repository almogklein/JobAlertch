import math
import numpy as np
import pandas as pd


class DataProcessor:
    """
    Class for processing data with various filters.
    """

    def __init__(self, window):
        """
        Constructor for DataProcessor.

        Parameters:
        - window: The window size for moving average filters.
        """
        self.flag = False
        self.window_size = window


    def low_pass_filter(self, data_buffer):
        """
        Apply low pass filter filter to the data.

        Parameters:
        - data_buffer: The input data buffer.

        Returns:
        - filtered_data: List of filtered data.
        """
    
        data_buffer = data_buffer[['X_ACC', 'Y_ACC', 'Z_ACC']]
        data_buffer = data_buffer.dropna(how='all')
        alpha = 0.05 #(self.window_size - 1) / (self.window_size)  # You can adjust the alpha value as needed

        if not data_buffer.empty:
            filtered_data = []
            for i in range(len(data_buffer)):
                if i == 0:
                    filtered_data.append([data_buffer.iloc[0, 0], data_buffer.iloc[0, 1], data_buffer.iloc[0, 2]])
                else:
                    current_x = (alpha) * data_buffer.iloc[i, 0] + (1 - alpha) * filtered_data[-1][0]
                    current_y = (alpha) * data_buffer.iloc[i, 1] + (1 - alpha) * filtered_data[-1][1]
                    current_z = (alpha) * data_buffer.iloc[i, 2] + (1 - alpha) * filtered_data[-1][2]
                    filtered_data.append([current_x, current_y, current_z])

            return pd.DataFrame(filtered_data, columns=data_buffer.columns)
        else:
            return pd.DataFrame()


    def simple_moving_average(self, data_buffer):
        """
        Apply simple moving average filter to the data frame.

        Parameters:
        - data_frame: The input data frame.
        - window_size: The size of the moving average window.

        Returns:
        - filtered_data: List of filtered data (X, Y, Z).
        """

        # Take only the required columns
        data_buffer = data_buffer[['X_ACC', 'Y_ACC', 'Z_ACC']]

        num_samples = len(data_buffer)
        filtered_data = []

        for i in range(0, num_samples - self.window_size):
            windowed_data = data_buffer.iloc[i:i + (self.window_size - 1)]
            window_average = windowed_data.mean().tolist()
            filtered_data.append(window_average)

        # Transpose the result to get separate lists for X, Y, Z
        filtered_data = list(map(list, zip(*filtered_data)))

        # Padding zeros to each sublist
        filtered_data[0] = [0]*(self.window_size) + filtered_data[0]
        filtered_data[1] = [0]*(self.window_size) + filtered_data[1]
        filtered_data[2] = [0]*(self.window_size) + filtered_data[2]

        return filtered_data
    
    def median_moving_average(self, data_buffer):
        """
        Apply median moving average filter to the data frame.

        Parameters:
        - data_buffer: The input data buffer.

        Returns:
        - filtered_data: List of filtered data (X, Y, Z).
        """

        # Take only the required columns
        data_buffer = data_buffer[['X_ACC', 'Y_ACC', 'Z_ACC']]

        num_samples = len(data_buffer)
        filtered_data = []

        for i in range(0, num_samples - self.window_size):
            windowed_data = data_buffer.iloc[i:i + (self.window_size - 1)]
            window_median = windowed_data.median().tolist()
            filtered_data.append(window_median)

        # Transpose the result to get separate lists for X, Y, Z
        filtered_data = list(map(list, zip(*filtered_data)))

        # Padding zeros to each sublist
        filtered_data[0] = [0]*self.window_size + filtered_data[0]
        filtered_data[1] = [0]*self.window_size + filtered_data[1]
        filtered_data[2] = [0]*self.window_size + filtered_data[2]

        return filtered_data

    def low_pass_filter_real_time(self, data_buffer, data_buffer_filtered):
        """
        Apply low pass filter filter to real-time data.

        Parameters:
        - data_buffer: The input real-time data buffer.
        - data_buffer_filtered: The filtered data buffer.

        Returns:
        - data_buffer_filtered: Filtered real-time data.
        """
        # Initialize the weights for the low_pass_filter
        alpha = 0.1 #(self.window_size - 1) / (self.window_size)

        # low_pass_filter for the real-time signal
        for i in range(len(data_buffer)):
            if i == 0:
                data_buffer_filtered.append([data_buffer[0][1], data_buffer[0][2], data_buffer[0][3]])
            else:
                current_x = ((alpha) * data_buffer[i][1]) + ((1 - alpha) * data_buffer_filtered[-1][0])
                current_y = ((alpha) * data_buffer[i][2]) + ((1 - alpha) * data_buffer_filtered[-1][1])
                current_z = ((alpha) * data_buffer[i][3]) + ((1 - alpha) * data_buffer_filtered[-1][2])

                data_buffer_filtered.append([current_x, current_y, current_z])

        return data_buffer_filtered

    def simple_moving_average_real_time(self, data_buffer, data_buffer_filtered):
        """
        Apply simple moving average filter to real-time data.

        Parameters:
        - data_buffer: The input real-time data buffer (queue of values).
        - data_buffer_filtered: The filtered data buffer (queue of averages).

        Returns:
        - data_buffer_filtered: Filtered real-time data.
        """
        window_sum = [0] * 3  # Initialize the sum for each position
        window_size = self.window_size

        for i in range(len(data_buffer)):
            for j in range(1, 4):
                window_sum[j-1] += data_buffer[i][j]
                
            # Calculate the moving average for each position and update the filtered buffer
            average_values = [window_sum[j] / min(i + 1, window_size) for j in range(3)]
            data_buffer_filtered.append(average_values)

        return data_buffer_filtered
    
    def manual_median(self, values):
        sorted_values = sorted(values)
        length = len(sorted_values)

        if length % 2 == 0:
            mid1 = sorted_values[length // 2 - 1]
            mid2 = sorted_values[length // 2]
            median_value = (mid1 + mid2) / 2
        else:
            median_value = sorted_values[length // 2]

        return median_value

    def median_moving_average_real_time(self, data_buffer, data_buffer_filtered):
        """
        Apply median moving average filter to real-time data.

        Parameters:
        - data_buffer: The input real-time data buffer (queue of values).
        - data_buffer_filtered: The filtered data buffer (queue of medians).

        Returns:
        - data_buffer_filtered: Filtered real-time data.
        """
        window_values = [[] for _ in range(1, 4)]  # Initialize window values for each position

        for i in range(len(data_buffer)):
            for j in range(1, 4):
                window_values[j-1].append(data_buffer[i][j])

            # Calculate the moving median for each position and update the filtered buffer
            median_values = [self.manual_median(window_values[j]) for j in range(3)]
            data_buffer_filtered.append(median_values)

        return data_buffer_filtered

    def calc_angal_of_signal(self, a_aidata_buffer_filtered, sr=0.1):

        l_aix = [data[0] for data in a_aidata_buffer_filtered]
        # l_aipace_of_change_x = [l_aix[index] - l_aix[index-1] for index in range(1, len(l_aix))]

        l_aiy = [data[1] for data in a_aidata_buffer_filtered]
        # l_aipace_of_change_y = [l_aiy[index] - l_aiy[index-1] for index in range(1, len(l_aiy))]

        l_aiz = [data[2] for data in a_aidata_buffer_filtered]
        # l_aipace_of_change_z = [l_aiz[index] - l_aiz[index-1] for index in range(1, len(l_aiz))]

        l_idt = sr*len(l_aix)
        # l_idt_pace = sr*len(l_aipace_of_change_x)

        l_idx = l_aix[-1] - l_aix[0]
        l_idy = l_aiy[-1] - l_aiy[0]
        l_idz = l_aiz[-1] - l_aiz[0]

        # l_idx_p = l_aipace_of_change_x[-1] - l_aipace_of_change_x[0]
        # l_idy_p = l_aipace_of_change_y[-1] - l_aipace_of_change_y[0]
        # l_idz_p = l_aipace_of_change_z[-1] - l_aipace_of_change_z[0]

        return [(l_idx/l_idt), (l_idy/l_idt), (l_idz/l_idt)] ##, [(l_idx_p/l_idt_pace), (l_idy_p/l_idt_pace), (l_idz_p/l_idt_pace)]