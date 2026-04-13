from spacecoords import celestial

lat, lon, alt = 67.1, 20.5, 420.0
latg, long, altg = celestial.geodetic_lla_to_geocentric_lla(lat, lon, alt, degrees=True)
lat0, lon0, alt0 = celestial.geocentric_lla_to_geodetic_lla(latg, long, altg, degrees=True)

print(lat, lon, alt)
print(latg, long, altg)
print(lat0, lon0, alt0)
