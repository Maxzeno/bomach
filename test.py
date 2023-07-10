from pyproj import Proj, transform

def dms_to_utm(latitude, longitude):
    # Define the source coordinate system (DMS)
    src_proj = Proj(init='EPSG:4326')  # EPSG:4326 is the WGS84 coordinate system (DMS)

    # Define the target coordinate system (UTM)
    target_proj = Proj(init='EPSG:32610')  # Example: UTM Zone 10N

    # Convert DMS to UTM
    easting, northing = transform(src_proj, target_proj, longitude, latitude)

    return easting, northing

def utm_to_dms(easting, northing, zone_number, zone_letter):
    # Define the source coordinate system (UTM)
    src_proj = Proj(proj='utm', zone=zone_number, ellps='WGS84', north=True if zone_letter >= 'N' else False)

    # Define the target coordinate system (DMS)
    target_proj = Proj(init='EPSG:4326')  # EPSG:4326 is the WGS84 coordinate system (DMS)

    # Convert UTM to DMS
    longitude, latitude = transform(src_proj, target_proj, easting, northing)

    return latitude, longitude

# Example usage for converting DMS to UTM
latitude_dms = (40, 30, 30)  # (degrees, minutes, seconds)
longitude_dms = (-74, 0, 21)  # (degrees, minutes, seconds)
easting, northing = dms_to_utm(latitude_dms, longitude_dms)
print("UTM Coordinates:", easting, northing)

# Example usage for converting UTM to DMS
easting_utm = 555111
northing_utm = 4466701
zone_num = 10
zone_letter = 'N'
latitude, longitude = utm_to_dms(easting_utm, northing_utm, zone_num, zone_letter)
print("DMS Coordinates:", latitude, longitude)
