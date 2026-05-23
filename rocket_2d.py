from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

# Parameters
mass      = 500
thrust    = 15000
burn_time = 10
Cd        = 0.3
A         = 0.05
rho       = 1.225
g         = 9.81
angle_deg = 45
angle_rad = np.radians(angle_deg)

def rocket_2d(t, y):
    x, y_pos, vx, vy = y

    speed = np.sqrt(vx**2 + vy**2)

    if t <= burn_time:
        T = thrust
    else:
        T = 0

    drag = 0.5 * rho * speed**2 * Cd * A

    if speed > 0:
        drag_x = -drag * vx / speed
        drag_y = -drag * vy / speed
    else:
        drag_x = 0
        drag_y = 0

    if t <= burn_time:
        ax = (T * np.cos(angle_rad) + drag_x) / mass
        ay = (T * np.sin(angle_rad) + drag_y) / mass - g
    else:
        ax = drag_x / mass
        ay = drag_y / mass - g

    return [vx, vy, ax, ay]

y0     = [0, 0, 0, 0]
t_span = (0, 60)
t_eval = np.linspace(0, 60, 1000)

sol = solve_ivp(rocket_2d, t_span, y0, t_eval=t_eval)

x   = sol.y[0]
alt = sol.y[1]

# find landing point
landing_idx = np.where(alt < 0)[0]
if len(landing_idx) > 0:
    landing_idx = landing_idx[0]
else:
    landing_idx = -1

plt.figure(figsize=(10, 5))
plt.plot(x[:landing_idx]/1000, alt[:landing_idx], 'b-', linewidth=2)
plt.xlabel('Horizontal distance (km)')
plt.ylabel('Altitude (m)')
plt.title(f'Rocket trajectory — launch angle {angle_deg}°')
plt.grid(True)
plt.tight_layout()
plt.savefig('rocket_2d.png', dpi=150)
plt.show()

print(f"Peak altitude: {alt.max():.1f} m")
print(f"Range: {x[landing_idx]/1000:.2f} km")