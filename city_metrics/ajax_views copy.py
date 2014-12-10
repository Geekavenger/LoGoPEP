from city_metrics.models import Energy, City
from city_metrics.views import getCities
import simplejson as json
from django.http import HttpResponse


def updateChart(request):
	json_data = {}
	chartError = False
	colLen = None
	linePosition = None
	series = None
	cityList = []
	timeList = []

	try:
		checkString = request.GET['aList']
	except Exception, e:
		chartError = e
		checkString = None

	if not chartError:
		strippedString = checkString.strip()
		newList = strippedString.split(",")

		chartType = request.GET['chartType']

		chartData = []
		averageList = []
		stats = None
		indicator = None

		for item in newList:

			if item.startswith('ind_'):
				term = item.replace('ind_','')

				indicator = term

			if item == 'All Central Cities' or item == 'All Inner Suburbs' or item == 'All Outer Suburbs':

				pass

			else:

				if item.startswith('city_'):
					cityID = item.replace('city_','')

					if cityID == 'all':
						cities = City.objects.all()
					else:
						cities = City.objects.filter(id=cityID)

					for city in cities:
						cityList.append(city)

			if item.startswith('time_'):
				year = item.replace('time_','')
				timeList.append(year)

			if item.startswith('average_'):
				average = item.replace('average_','')
				averageList.append(average)

		chartTitles = getChartTitles(cityList, averageList)

		chartData.append(chartTitles)

		if chartType == 'energy':
			stats = Energy.objects.all()

		try:
			cityStats = stats.filter(city__in=cityList, year__in=timeList).order_by('year')

		except Exception, e:
			print e
			cityStats = stats

		if len(cityList) > 0 and len(timeList) > 0:

			chartData, colLen, linePosition = getChartData(stats, indicator, chartData, cityStats, timeList, averageList)

			series = buildSeries(colLen, linePosition)

		else:
			chartData = [
				['Year', 'none'],
				['none',    0],
			]


	else:
		chartData = [
			['Year', 'none'],
			['none',    0],
		]

	json_data['columns'] = chartData
	json_data['series'] = series

	subTitleCities = []
	if len(cityList) > 0:

		for city in cityList:

			cityString = ' ' + str(city.city)

			subTitleCities.append(cityString)

	json_data['cities'] = subTitleCities

	if timeList[0] == 'all':

		listLen = len(timeList) - 1

		titleYears = timeList[1] + '-' + timeList[listLen]

		json_data['years'] = titleYears

	else:
		json_data['years'] = timeList

	return HttpResponse(json.dumps(json_data), mimetype='application/json')




def getChartTitles(cityList, averageList):

	try:
		chartTitles = ['year',]
		for city in cityList:
			cityName = city.city
			chartTitles.append(str(cityName))

		title = None
		if len(averageList) > 0:

			for average in averageList:
				if average == 'central':
					title = 'Central City Average'

				if average == 'inner':
					title = 'Inner Suburbs Average'

				if average == 'outer':
					title = 'Outer Suburbs Average'

				if average == 'state':
					title = 'MN State Average'

				if average == 'us':
					title = 'US Average'

				if title:
					chartTitles.append(title)

	except Exception, e:
		print e
		chartTitles = ['year',]

	return chartTitles




def getChartData(stats, indicator, chartData, cityStats, timeList, averageList):

	year = None
	chartStatCol = []
	aveList = []
	statisticSum = 0
	statisticAverage = None

	for stat in cityStats:

		if indicator == 'total energy source':
			statistic = stat.electricity_res + stat.electricity_com_ind + stat.therms_res + stat.therms_com_ind

		elif indicator == 'total energy type':
			statistic = stat.res_energy + stat.com_ind_energy

		elif indicator == 'res energy cons':
			statistic = stat.res_energy

		elif indicator == 'com energy cons':
			statistic = stat.com_ind_energy


		if year == None or year == stat.year:
			year = stat.year

			if len(chartStatCol) < 1:
				chartStatCol.append(str(year))

			chartStatCol.append(int(statistic))

			## Get Averages If Needed ##
			count = 0
			statisticSum = 0
			statisticAverage = None

			if len(averageList) > 0:
				for ave in averageList:

					if ave == 'state':
						if stat.year == '2008':
							statisticSum = 2840
							count = 1

						if stat.year == '2009':
							statisticSum = 2670
							count = 1

						if stat.year == '2010':
							statisticSum = 2750
							count = 1

					if ave == 'us':
						if stat.year == '2008':
							statisticSum = 2760
							count = 1

						if stat.year == '2009':
							statisticSum = 2920
							count = 1

						if stat.year == '2010':
							statisticSum = 2890
							count = 1

					else:

						for object in stats:

							if object.year == stat.year:

								if ave == 'central':
									if object.city.type == 'C':
										statisticSum = statisticSum + object.electricity_res + object.electricity_com_ind + object.therms_res + object.therms_com_ind
										count += 1

								if ave == 'inner':
									if object.city.type == 'I':
										statisticSum = statisticSum + object.electricity_res + object.electricity_com_ind + object.therms_res + object.therms_com_ind
										count += 1

								if ave == 'outer':
									if object.city.type == 'O':
										statisticSum = statisticSum + object.electricity_res + object.electricity_com_ind + object.therms_res + object.therms_com_ind
										count += 1

					if not statisticAverage and statisticSum > 0 and len(aveList) < len(averageList):
						divNum = count

						statisticAverage = statisticSum/divNum
						aveList.append(statisticAverage)

						statisticSum = 0
						statisticAverage = None

		else:

			if len(aveList) > 0:

				for i in aveList:
					chartStatCol.append(int(i))

				aveList = []

			chartData.append(chartStatCol)

			year = stat.year

			chartStatCol = []
			if len(chartStatCol) < 1:
				chartStatCol.append(str(year))

			chartStatCol.append(int(statistic))

	if len(aveList) > 0:

		for i in aveList:
			chartStatCol.append(int(i))

		subNum = len(aveList) + 1

		colLen = len(chartStatCol) - subNum

	else:
		colLen = len(chartStatCol) - 1

	chartData.append(chartStatCol)

	return chartData, colLen, aveList




def buildSeries(colLen, aveList):

	color = 'color'
	type = 'type'

	bar_color_options, line_color_options = colorCodes()

	series = {}

	position = 0
	for i in range(0,colLen):
		series[i] = {color: bar_color_options[i]}
		position = position + 1

	if len(aveList) > 0:

		lineOption = 0
		for i in aveList:
			series[position] = {type: "line", color: line_color_options[lineOption]}
			lineOption = lineOption + 1
			position = position + 1

	return series




def colorCodes():

	bar_color_options = ['#e97c46','#e97c46','#e97c46','#e97c46','#e97c46']

	line_color_options = ['#B73100','#B73184','#8243B5','#3E4CB5','#3AAFB5']

	return bar_color_options, line_color_options