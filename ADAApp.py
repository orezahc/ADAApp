import simplejson
import urllib.parse
import urllib.request

DIRECTION_BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json'
THE_Y = '47.245399,-122.439856'
TACOMA_MALL = '47.218132, -122.467618'

def getRoute(origin, destination):
  args = {
      'mode':'transit',
      'origin':origin,
      'destination':destination,
      'alternatives':'true'
      }
  url = DIRECTION_BASE_URL + '?' + urllib.parse.urlencode(args)
  response = simplejson.load(urllib.request.urlopen(url))

  results = []
  if response['status'] != 'OK': return None

  for route in response['routes']:
    result = []
    for step in route['legs'][0]['steps']:
      if step['travel_mode'] == 'WALKING':
        for portion in step['steps']:
          start = portion['start_location']
          end = portion['end_location']
          distance = portion['distance']['value']
          result.extend(getSlope(start['lat'], start['lng'], end['lat'], end['lng'], distance))
          #result.append((start['lat'], start['lng'], end['lat'], end['lng'], distance))
    results.append(result)

  return results


ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json'
CHART_BASE_URL = 'http://chart.apis.google.com/chart'

def getElevation(path="36.578581,-118.291994|36.23998,-116.83171",samples="100", **elvtn_args):
  # elvtn_args.update({'path': path,'samples': samples})
  args = {'samples': samples,'path': path}
  url = ELEVATION_BASE_URL + '?' + urllib.parse.urlencode(args)

  response = simplejson.load(urllib.request.urlopen(url))
  # # print url
  # # Create a dictionary for each results[] object
  elevationArray = []

  for resultset in response['results']:
    elevationArray.append(resultset['elevation'])

  # # Create the chart passing the array of elevation data

  return elevationArray
  # return [1,2]
  # return getChart(chartData=elevationArray)

def getSlope(startx, starty, destinationx, destinationy, length):
  samples = length / 10 + 2
  uLength = float(length)/float(samples)
  # print length
  # print samples
  # print length%10
  result = getElevation("%s,%s|%s,%s"%(startx, starty, destinationx, destinationy), samples = "%d"%samples)
  slope = [(y - x)/uLength for x,y in zip(result, result[1:])]

  # print result
  # print slope
  return slope

if __name__ == '__main__':
    # # Mt. Whitney
    # startStr = "36.578581,-118.291994"
    # # Death Valley
    # endStr = "36.23998,-116.83171"

    # pathStr = startStr + "|" + endStr

    # getElevation(pathStr)
    ret = getSlope('36.578581','-118.291994','36.23998','-116.83171',1008)
    for x in ret:
      print(x)
