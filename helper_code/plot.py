import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from scipy.signal import medfilt
import os

window_size = 10
filter_choice = "moving_average"

def moving_average(data, window_size):
		return np.convolve(data, np.ones(window_size), 'valid') / window_size

def plot_data(main_folder):
				os.chdir("../" + main_folder)
				# Path to the main folder containing subfolders

				# Get a list of all electrode folders
				electrode_folders = [f.path for f in os.scandir("./") if f.is_dir()]
				for electrode_folder in electrode_folders:
								print(electrode_folder) 
								test_set_folders = [f.path for f in os.scandir("./" + electrode_folder)]
								# Loop through each subfolder
								for test_set in test_set_folders:
										# Create a new figure for each subfolder
										plt.figure(figsize=(10, 6))

										# Get a list of all CSV files in the subfolder
										csv_files = glob.glob(f"{test_set}/*.csv")

										# Loop through each CSV file in the subfolder
										for file in csv_files:
												# Read the CSV file
												data = pd.read_csv(file)

												# Extract the columns
												v = data['volts']
												c = data['current']
												label = data['minutes_in_buffer'].iloc[0]  # Get the first row of the time_buffer column

												# Apply selected filter
												if filter_choice == "median":
														v = medfilt(v, window_size)
														c = medfilt(c, window_size)
												elif filter_choice == "moving_average":
														v = moving_average(v, window_size)
														c = moving_average(c, window_size)

												# Remove negative values from current (y-axis)
												valid_data = c >= 0
												v = v[valid_data]
												c = c[valid_data]

												# Plot C vs V if there are remaining valid data points
												if len(v) > 0:
														plt.plot(v, c, label=f"{label}")

										# Add labels, title, and legend
										plt.xlabel("V (Voltage)")
										plt.ylabel("uA (Current)")
										plt.title(f"{os.path.basename(test_set)} - Filter: {filter_choice.capitalize()}")
										plt.legend()

										# Customize grid with 0.1 intervals for both x and y axes
										plt.grid(True)

										# Set the grid line intervals
										plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.1))  # For x-axis gridlines at .1 intervals
										plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.1))  # For y-axis gridlines at .1 intervals

										# Adjust layout and save the plot
										plt.tight_layout()
										plt.savefig(f"{test_set}.png")
										# plt.close()  # Close the figure to free up memory
										plt.show(block=False)

								print("Plots have been saved in their respective subfolders.")

