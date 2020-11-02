# Copyright 2020, Robert Kight
#
# Fetch and parse a weather report from the Internet.
require 'net/http'
require 'json'
require 'date'

def bearing_to_compass(b)
  # List of possible compass directions and their bearing in degrees.
  direction = {n: 0, ne: 45, e: 90, se: 135, s: 180, sw: 225, w: 270, nw: 315}

  # Because Bearing can be anything from 0 to 359, we need to cycle through them. Let's start with North.
  
  cur_dir = 'n' #<- Keep track of which compass direction we're on.
  direction.each do |k, v|

    # If the bearing value is greater than the direction we're currently on, update the value.
    if b > v
      cur_dir = k
    end
  end

  # Return the uppercase value.
  return cur_dir.upcase
end


key = "your-key-here"
#lat = "41.1590783" <- change this
#lon = "-75.1271883" <- change this

uri = URI("https://api.darksky.net/forecast/#{key}/#{lat},#{lon}")

ds_json = Net::HTTP.get(uri)
ds_hash = JSON.parse(ds_json, symbolize_names: true)

# Report hash
report = {}

report_date_raw = ds_hash[:currently][:time]
#DateTime.strftime("1318996912", '%s')
report_date = Time.at(report_date_raw)

report[:date] = report_date.strftime('"%I:%M%P on %A, %B %d, %Y"')
report[:rain_chance] = "Rain chance: " + (ds_hash[:daily][:data][0][:precipProbability] * 100).to_s
report[:condition] = "Summary: " + ds_hash[:currently][:summary]
report[:temp_cur] = "Current temperature: " + ds_hash[:currently][:temperature].to_s + "F"
report[:temp_hi] = "High today: " + ds_hash[:daily][:data][0][:temperatureHigh].to_s + "F"
report[:temp_lo] = "Low today: " + ds_hash[:daily][:data][0][:temperatureLow].to_s + "F"
report[:wind_speed] = "Wind speed: " + ds_hash[:currently][:windSpeed].to_s + "mph"
report[:wind_direction] = "Wind direction: " + bearing_to_compass(ds_hash[:currently][:windBearing]).to_s

# Add more information to your report using the above code as an example.

report.each do |k,v|
	puts v.to_s
end
