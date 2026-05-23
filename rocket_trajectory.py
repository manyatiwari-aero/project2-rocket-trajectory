from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

#Rocket parameters
mass = 500 # kg
thrust = 15000 #N
burn_time = 10 # seconds
Cd = 0.3 # Drag coefficient
A = 0.05 # m^2 reference area
rho = 1.225 # kg/m^3 air density    
g = 9.81 #gravity m/s^2

#Physics function
def rocket(t, y):
    altitude = y[0]
    velocity = y[1]
    
    #thrust is only applied during burn time
    if t < burn_time:
        T = thrust
    else:
        T = 0
    
    #Drag always opposes the motion
    drag = 0.5 * rho * velocity**2 * Cd * A
    if velocity < 0:
        drag = -drag
    
    #net acceleration newtons 2nd law
    acceleration = (T - drag)/mass - g

    return [velocity, acceleration]

# ── Run simulation ─────────────────────────────────
y0     = [0, 0]                        # starts at 0m, 0 m/s
t_span = (0, 60)                       # simulate 60 seconds
t_eval = np.linspace(0, 60, 1000)     # 1000 time points

sol = solve_ivp(rocket, t_span, y0, t_eval=t_eval)

# ── Plot results ───────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].plot(sol.t, sol.y[0], 'b-', linewidth=2)
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Altitude (m)')
axes[0].set_title('Rocket — altitude')
axes[0].grid(True)
axes[0].axvline(x=burn_time, color='r',
                linestyle='--', label='Burnout')
axes[0].legend()

axes[1].plot(sol.t, sol.y[1], 'r-', linewidth=2)
axes[1].set_xlabel('Time (s)')
axes[1].set_ylabel('Velocity (m/s)')
axes[1].set_title('Rocket — velocity')
axes[1].grid(True)
axes[1].axvline(x=burn_time, color='r',
                linestyle='--', label='Burnout')
axes[1].legend()

plt.tight_layout()
plt.savefig('rocket_trajectory.png', dpi=150)
plt.show()

# ── Print results ──────────────────────────────────
peak_alt = sol.y[0].max()
peak_vel = sol.y[1].max()
print(f"Peak altitude: {peak_alt:.1f} m")
print(f"Peak velocity: {peak_vel:.1f} m/s")