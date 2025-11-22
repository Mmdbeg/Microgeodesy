import math

def dms_to_deg(d, m, s):
    return d + m/60 + s/3600

def deg_to_dms(deg):
    deg = deg % 360
    d = int(deg)
    m = int((deg - d) * 60)
    s = (deg - d - m/60) * 3600
    return f"{d}° {m}' {s:.1f}\""

def zero_by_br4(series):
    """همهٔ زوایا را طوری جابه‌جا می‌کند که BR4 = 0 شود"""
    br4_value = dms_to_deg(*series["BR4"])
    adjusted = {}
    for name, (d, m, s) in series.items():
        a = dms_to_deg(d, m, s)
        new_a = (a - br4_value) % 360
        adjusted[name] = deg_to_dms(new_a)
    return adjusted

# -------------------
# data
# -------------------

series1 = {
    "BL4": (86, 49, 1.7),
    "BL5": (117, 43, 44.0),
    "BR4": (189, 14, 2.1),
    "BC3": (52, 47, 34.1),
}

series2 = {
    "BR3": (215, 41, 11.6),
    "BR4": (139, 17, 22.7),
    "BR6": (112, 24, 0.7),
}

# هر دو سری به BR4 صفر میشن
adj1 = zero_by_br4(series1)
adj2 = zero_by_br4(series2)

# -------------------
# نمایش نتایج
# -------------------
print("سری اول (BR4=0):")
for k, v in adj1.items():
    print(f"{k}: {v}")

print("\nسری دوم (BR4=0):")
for k, v in adj2.items():
    print(f"{k}: {v}")

