<!DOCTYPE html>
<html>
<head>
  <title>Create Identical Form Field</title>
  <style>
    .form-field {
      margin-bottom: 10px;
    }
  </style>
</head>
<body>
  <form>
    <div class="form-field">
      <label for="field1">Field 1:</label>
      <input type="text" onclick="createIdenticalFormField()" id="field1" name="field1">
    </div>
    <button type="button">Add Field</button>
  </form>

  <script>
    function createIdenticalFormField() {
      var form = document.querySelector('form');
      var lastFormField = document.querySelector('.form-field:last-child');

      var newFormField = lastFormField.cloneNode(true);
      var newFieldId = 'field' + (parseInt(lastFormField.querySelector('input').id.slice(-1)) + 1);
      newFormField.querySelector('label').setAttribute('for', newFieldId);
      newFormField.querySelector('input').setAttribute('id', newFieldId);
      newFormField.querySelector('input').setAttribute('name', newFieldId);

      form.appendChild(newFormField);
    }
  </script>
</body>
</html>












from pyproj import Proj

def convert_easting_northing_to_lon_lat(easting, northing):
    # Define the projection system for Nigeria
    nigeria_proj = Proj(proj='utm', zone=31, ellps='WGS84', south=False)
    
    # Convert Easting/Northing to Longitude/Latitude
    lon, lat = nigeria_proj(easting, northing, inverse=True)
    
    return lon, lat

# Example usage
easting = 300000  # Example Easting value
northing = 400000  # Example Northing value

lon, lat = convert_easting_northing_to_lon_lat(easting, northing)
print(f"Longitude: {lon}, Latitude: {lat}")



def convert_decimal_to_dms(decimal):
    degrees = int(decimal)
    decimal_minutes = abs(decimal - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = (decimal_minutes - minutes) * 60
    
    return degrees, minutes, seconds









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
