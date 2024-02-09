v_air = 0.18
def get_calculate_hc(v):
    if v< 0.2:
        h_c = 3.1  # [W/m^2*K]
    elif 0.2 <= v <= 4:
        h_c = 8.1 * (v ** 0.6)
    else:
        h_c = 0
    return h_c

print(get_calculate_hc(v_air))