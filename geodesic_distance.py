import math
import tkinter as tk
from tkinter import messagebox

def geodesic_dist(lat1, lon1, lat2, lon2):
    
    f = 1 / 298.257223563  
    b = 6356752.3142  
    a = 6378137  

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    U1 = math.atan((1 - f) * math.tan(lat1))
    U2 = math.atan((1 - f) * math.tan(lat2))
    L = lon2 - lon1

    sinU1, cosU1 = math.sin(U1), math.cos(U1)
    sinU2, cosU2 = math.sin(U2), math.cos(U2)
    lambda_old = L
    iteration_limit = 1000

    for _ in range(iteration_limit):
        sin_lambda = math.sin(lambda_old)
        cos_lambda = math.cos(lambda_old)
        sin_sigma = math.sqrt((cosU2 * sin_lambda) ** 2 +
                              (cosU1 * sinU2 - sinU1 * cosU2 * cos_lambda) ** 2)
        cos_sigma = sinU1 * sinU2 + cosU1 * cosU2 * cos_lambda
        sigma = math.atan2(sin_sigma, cos_sigma)
        sin_alpha = cosU1 * cosU2 * sin_lambda / sin_sigma
        cos_square_alpha = 1 - sin_alpha ** 2
        cos_2_sigmaM = cos_sigma - 2 * sinU1 * sinU2 / cos_square_alpha if cos_square_alpha != 0 else 0
        C = f / 16 * cos_square_alpha * (4 + f * (4 - 3 * cos_square_alpha))
        lambda_new = L + (1 - C) * f * sin_alpha * (
            sigma + C * sin_sigma * (cos_2_sigmaM + C * cos_sigma * (-1 + 2 * cos_2_sigmaM ** 2))
        )

        if abs(lambda_new - lambda_old) < 1e-12:
            break
        lambda_old = lambda_new

    u_square = cos_square_alpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + u_square / 16384 * (4096 + u_square * (-768 + u_square * (320 - 175 * u_square)))
    B = u_square / 1024 * (256 + u_square * (-128 + u_square * (74 - 47 * u_square)))
    delta_sigma = B * sin_sigma * (
        cos_2_sigmaM + B / 4 * (cos_sigma * (-1 + 2 * cos_2_sigmaM ** 2) -
                                B / 6 * cos_2_sigmaM * (-3 + 4 * sin_sigma ** 2) * (-3 + 4 * cos_2_sigmaM ** 2)))
    s = b * A * (sigma - delta_sigma)

    return s / 1000  


def calculate_distance():
    try:
        
        lat1 = float(entry_lat1.get())
        lon1 = float(entry_lon1.get())
        lat2 = float(entry_lat2.get())
        lon2 = float(entry_lon2.get())

        if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90 and -180 <= lon1 <= 180 and -180 <= lon2 <= 180):
            raise ValueError("Coordinates are out of valid range.")

        distance = geodesic_dist(lat1, lon1, lat2, lon2)
        result_label.config(text=f"Distance: {distance:.2f} km")
    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error: {e}")


root = tk.Tk()
root.title("Geodesic Distance Calculator")

tk.Label(root, text="Latitude 1").grid(row=0, column=0, padx=5, pady=5)
entry_lat1 = tk.Entry(root)
entry_lat1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Longitude 1").grid(row=1, column=0, padx=5, pady=5)
entry_lon1 = tk.Entry(root)
entry_lon1.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Latitude 2").grid(row=2, column=0, padx=5, pady=5)
entry_lat2 = tk.Entry(root)
entry_lat2.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Longitude 2").grid(row=3, column=0, padx=5, pady=5)
entry_lon2 = tk.Entry(root)
entry_lon2.grid(row=3, column=1, padx=5, pady=5)

calculate_button = tk.Button(root, text="Calculate Distance", command=calculate_distance)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Distance: ", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
