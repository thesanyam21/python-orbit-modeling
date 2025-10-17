"""
orbit_simulation.py
Author: Sanyam Kukreja

Simulates a 2D elliptical orbit of a satellite around Earth using
Newtonian mechanics and the Runge–Kutta 4th order (RK4) integration method.
Plots the resulting orbit trajectory and prints key orbital parameters.
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11         # gravitational constant (m^3 kg^-1 s^-2)
M_earth = 5.972e24      # mass of Earth (kg)
R_earth = 6.371e6       # radius of Earth (m)

# Initial conditions
r0 = np.array([R_earth + 700e3, 0])   # initial position (700 km altitude)
v0 = np.array([0, 7500])              # initial velocity (m/s)
state = np.concatenate((r0, v0))

# Simulation parameters
dt = 1.0     # time step (s)
t_max = 6000 # total simulation time (s)

def acceleration(r):
    """Compute gravitational acceleration vector."""
    r_mag = np.linalg.norm(r)
    return -G * M_earth * r / r_mag**3

def rk4_step(state, dt):
    """Perform a single Runge–Kutta 4th order integration step."""
    r = state[0:2]
    v = state[2:4]

    k1r = v
    k1v = acceleration(r)

    k2r = v + 0.5 * dt * k1v
    k2v = acceleration(r + 0.5 * dt * k1r)

    k3r = v + 0.5 * dt * k2v
    k3v = acceleration(r + 0.5 * dt * k2r)

    k4r = v + dt * k3v
    k4v = acceleration(r + dt * k3r)

    r_new = r + (dt / 6.0) * (k1r + 2*k2r + 2*k3r + k4r)
    v_new = v + (dt / 6.0) * (k1v + 2*k2v + 2*k3v + k4v)

    return np.concatenate((r_new, v_new))

# Arrays to store trajectory
trajectory = []
for t in np.arange(0, t_max, dt):
    trajectory.append(state[0:2])
    state = rk4_step(state, dt)

trajectory = np.array(trajectory)

# Calculate semi-major axis, orbital period, and eccentricity
r_mag = np.linalg.norm(r0)
v_mag = np.linalg.norm(v0)
mu = G * M_earth

# Semi-major axis
a = 1 / ((2 / r_mag) - (v_mag**2 / mu))

# Orbital period
T = 2 * np.pi * np.sqrt(a**3 / mu)

# Eccentricity calculation
# Extend vectors to 3D for np.cross
r0_3d = np.append(r0, 0)
v0_3d = np.append(v0, 0)
h_vec = np.cross(r0_3d, v0_3d)                # angular momentum vector
h_mag = np.linalg.norm(h_vec)

# Eccentricity magnitude
ecc = np.sqrt(1 - (h_mag**2) / (mu * a))

print(f"Semi-major axis (a): {a/1000:.2f} km")
print(f"Orbital period (T): {T/60:.2f} minutes")
print(f"Eccentricity (e): {ecc:.3f}")

# Plot results
plt.figure(figsize=(6,6))
plt.plot(trajectory[:,0]/1e3, trajectory[:,1]/1e3, label="Satellite Trajectory")
circle = plt.Circle((0, 0), R_earth/1e3, color='blue', alpha=0.4, label='Earth')
plt.gca().add_patch(circle)
plt.title("Elliptical Orbit Simulation - Sanyam Kukreja")
plt.xlabel("x-position (km)")
plt.ylabel("y-position (km)")
plt.axis("equal")
plt.legend()
plt.grid(True)
plt.show()
