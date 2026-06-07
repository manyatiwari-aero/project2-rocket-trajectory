import numpy as np
import matplotlib.pyplot as plt

def isa_atmosphere(h):
    """
    International Standard Atmosphere model.
    h: altitude in meteres (0 to 20000 m)
    Returns: temperature (K), pressure (Pa), density ()
    """
    # Sea level standard values
    T0   = 288.15   # K - 15 C
    P0   = 101325   # Pa - standard sea level pressure
    rho0 = 1.225    # kg/m^3 
    L    = 0.0065   # K/m - temperature lapse rate
    R    = 287.05   # J/(kg.K) - gas constant for air
    g    = 9.81     # m/s^2   

    #convert h to array if single value 
    h = np.atleast_1d(np.array(h, dtype=float))

    T    = np.zeros_like(h)
    P    = np.zeros_like(h)
    rho  = np.zeros_like(h)

    #Layer 1: Troposphere 0 to 11000 m
    tropo = h <= 11000
    T[tropo]   = T0 - L * h[tropo]
    P[tropo]   = P0 * (T[tropo] / T0) ** (g / (L * R))
    rho[tropo] = P[tropo] / (R * T[tropo])

    #Layer 2: Stratosphere 11000 to 20000 m
    # temperature constant at 216.65 K 
    T11   = 216.65
    P11   = 22632.1    # Pa — exact value at 11km from standard tables
    rho11 = P11 / (R * T11)
    strato = h > 11000
    T[strato]   = T11
    P[strato]   = P11 * np.exp(-g * (h[strato] - 11000) / (R * T11))
    rho[strato] = P[strato] / (R * T[strato])
    return T, P, rho
#-------- General data -----------
h = np.linspace(0, 20000, 500)
T, P, rho = isa_atmosphere(h)

#-------- Plotting -----------
fig, axes = plt.subplots(1, 3, figsize=(14, 5))

# Temperature 
axes[0].plot(T - 273.15, h/1000, 'r-', linewidth=2)
axes[0].set_xlabel('Temperature (°C)')
axes[0].set_ylabel('Altitude (km)')
axes[0].set_title('ISA - Temperature')
axes[0].axhline(y=11, color='k', linestyle='--', linewidth=1, label='Tropospause (11km)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Pressure
axes[1].plot(P/1000, h/1000, 'b-', linewidth=2)
axes[1].set_xlabel('Pressure (kPa)')
axes[1].set_ylabel('Altitude (km)')
axes[1].set_title('ISA - Pressure')
axes[1].axhline(y=11, color='k', linestyle='--', linewidth=1, label='Tropospause (11km)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Density
axes[2].plot(rho, h/1000, 'g-', linewidth=2)
axes[2].set_xlabel('Density (kg/m³)')
axes[2].set_ylabel('Altitude (km)')
axes[2].set_title('ISA - Density')
axes[2].axhline(y=11, color='k', linestyle='--', linewidth=1, label='Tropospause (11km)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.suptitle('International Standard Atmosphere (ISA)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('isa_atmosphere.png', dpi=150, bbox_inches='tight')
plt.show()

#------Print key values -------
print("ISA Standard Values:")
print(f"{'Altitude':>10} {'Temp (°C)':>12} "
      f"{'Pressure (kPa)':>16} {'Density (kg/m³)':>16}")
print("-" * 58)

checkpoints = [0, 2000, 4000, 6000, 8000,
               10000, 11000, 15000, 20000]
for alt in checkpoints:
    T_val, P_val, rho_val = isa_atmosphere(alt)
    print(f"{alt:>10.0f} {T_val[0]-273.15:>12.2f} "
          f"{P_val[0]/1000:>16.3f} {rho_val[0]:>16.4f}")