import simplejson
import urllib.parse
import urllib.request

ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json'
CHART_BASE_URL = 'http://chart.apis.google.com/chart'

def getChart(chartData, chartDataScaling="-500,5000", chartType="lc",chartLabel="Elevation in Meters",chartSize="500x160",chartColor="orange", **chart_args):
    chart_args.update({
      'cht': chartType,
      'chs': chartSize,
      'chl': chartLabel,
      'chco': chartColor,
      'chds': chartDataScaling,
      'chxt': 'x,y',
      'chxr': '1,-500,5000'
    })



    dataString = 't:' + ','.join(str(x) for x in chartData)
    chart_args['chd'] = dataString.strip(',')
    return chartData


def getElevation(path="36.578581,-118.291994|36.23998,-116.83171",samples="100", **elvtn_args):
	# elvtn_args.update({'path': path,'samples': samples})
	args = {'samples': samples,'path': path}
	url = ELEVATION_BASE_URL + '?' + urllib.parse.urlencode(args)

	response = simplejson.load(urllib.request.urlopen(url))
	# # print url
	# # Create a dictionary for each results[] object
	# elevationArray = []

	# for resultset in response['results']:
	# 	elevationArray.append(resultset['elevation'])

	# # Create the chart passing the array of elevation data

	return elevationArray
	# return [1,2]
	# return getChart(chartData=elevationArray)

def getSlope(startx, starty, destinationx, destinationy, length):
	samples = length / 10 + 1
	# print length
	# print samples
	# print length%10
	result = getElevation("%f,%f|%f,%f"%(startx, starty, destinationx, destinationy), samples = "%d"%samples)
	slope = [(y - x)/10 for x,y in zip(result, result[1:])]

	if length % 10 != 0:
		slope[-1] = (result[-2]-result[-1])/(length%10)
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
    ret = getSlope(36.578581,-118.291994,36.23998,-116.83171,1008)
    for x in ret:
    	print(x)