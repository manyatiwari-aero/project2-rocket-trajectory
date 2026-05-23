from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

mass=500; thrust=15000; burn_time=10
Cd=0.3; A=0.05; rho=1.225; g=9.81

def rocket_2d(t, y, angle_rad):
    x, y_pos, vx, vy = y
    speed = np.sqrt(vx**2 + vy**2)
    T = thrust if t <= burn_time else 0
    drag = 0.5 * rho * speed**2 * Cd * A
    drag_x = -drag * vx/speed if speed>0 else 0
    drag_y = -drag * vy/speed if speed>0 else 0
    if t <= burn_time:
        ax = (T*np.cos(angle_rad) + drag_x)/mass
        ay = (T*np.sin(angle_rad) + drag_y)/mass - g
    else:
        ax = drag_x/mass
        ay = drag_y/mass - g
    return [vx, vy, ax, ay]

angles = range(10, 85, 1)
ranges = []

for angle_deg in angles:
    angle_rad = np.radians(angle_deg)
    y0 = [0,0,0,0]
    sol = solve_ivp(
        lambda t,y: rocket_2d(t,y,angle_rad),
        (0,120), y0,
        t_eval=np.linspace(0,120,2000)
    )
    alt = sol.y[1]
    x   = sol.y[0]
    landing = np.where(alt < 0)[0]
    if len(landing) > 0:
        ranges.append(x[landing[0]]/1000)
    else:
        ranges.append(x[-1]/1000)

best_angle = list(angles)[np.argmax(ranges)]
best_range = max(ranges)

plt.figure(figsize=(8,5))
plt.plot(list(angles), ranges, 'bo-', linewidth=2, markersize=6)
plt.axvline(x=best_angle, color='r', linestyle='--',
            label=f'Best angle: {best_angle}°')
plt.xlabel('Launch angle (degrees)')
plt.ylabel('Range (km)')
plt.title('Rocket range vs launch angle')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('parametric_study.png', dpi=150)
plt.show()

print(f"Best launch angle: {best_angle}°")
print(f"Maximum range: {best_range:.2f} km")