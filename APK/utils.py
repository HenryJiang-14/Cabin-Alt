P0 = 1013.25

def pressure_to_altitude_ft(pressure):
    altitude_m = 44330 * (1 - (pressure / P0) ** 0.1903)
    return altitude_m * 3.28084