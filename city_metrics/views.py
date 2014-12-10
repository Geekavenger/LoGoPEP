from django.shortcuts import render_to_response
from city_metrics.models import City, Energy, Water, Travel, Waste, Emissions, Cost
from utility import setDetailContext


def viewEnergyChart(request, page):
    chartType = 'energy'
    chartColor = '#F18C39'
    weather = True

    centralCities, innerCities, outerCities = getCities(request)

    chartData = []

    yearRange = []

    energyObjects = Energy.objects.all().order_by('year')
    year = ''
    for object in energyObjects:

        if year != object.year:
            yearRange.append(object.year)
            year = object.year

        else:
            pass

    if year != '':
        start_year = year

    else:
        start_year = None

    context = {'page': page, 'chartType': chartType, 'chartColor': chartColor, 'chartData': chartData,
               'centralCities': centralCities, 'innerCities': innerCities, 'outerCities': outerCities,
               'yearRange': yearRange, 'weather': weather, 'start_year': start_year}
    setDetailContext(context)

    return render_to_response('charts/energy.html', context)


def viewWaterChart(request, page):
    chartType = 'water'
    chartColor = '#8DC6EB'

    centralCities, innerCities, outerCities = getCities(request)

    chartData = []

    yearRange = []

    waterObjects = Water.objects.all().order_by('year')
    year = ''
    for object in waterObjects:

        if year != object.year:
            yearRange.append(object.year)
            year = object.year

        else:
            pass

    if year != '':
        start_year = year

    else:
        start_year = None

    context = {'page': page, 'chartType': chartType, 'chartColor': chartColor, 'chartData': chartData,
               'centralCities': centralCities, 'innerCities': innerCities, 'outerCities': outerCities,
               'yearRange': yearRange, 'start_year': start_year}
    setDetailContext(context)

    return render_to_response('charts/water.html', context)


def viewTravelChart(request, page):
    chartType = 'travel'
    chartColor = '#96C94D'

    centralCities, innerCities, outerCities = getCities(request)

    chartData = []

    yearRange = []

    travelObjects = Travel.objects.all().order_by('year')
    year = ''
    for object in travelObjects:

        if year != object.year:
            yearRange.append(object.year)
            year = object.year

        else:
            pass

    if year != '':
        start_year = year

    else:
        start_year = None

    context = {'page': page, 'chartType': chartType, 'chartColor': chartColor, 'chartData': chartData,
               'centralCities': centralCities, 'innerCities': innerCities, 'outerCities': outerCities,
               'yearRange': yearRange, 'start_year': start_year}
    setDetailContext(context)

    return render_to_response('charts/travel.html', context)


def viewWasteChart(request, page):
    chartType = 'waste'
    chartColor = '#8B61A1'

    centralCities, innerCities, outerCities = getCities(request)

    chartData = []

    yearRange = []

    wasteObjects = Waste.objects.all().order_by('year')
    year = ''
    for object in wasteObjects:

        if year != object.year:
            yearRange.append(object.year)
            year = object.year

        else:
            pass

    if year != '':
        start_year = year

    else:
        start_year = None

    context = {'page': page, 'chartType': chartType, 'chartColor': chartColor, 'chartData': chartData,
               'centralCities': centralCities, 'innerCities': innerCities, 'outerCities': outerCities,
               'yearRange': yearRange, 'start_year': start_year}
    setDetailContext(context)

    return render_to_response('charts/waste.html', context)


def viewEmissionsChart(request, page):
    chartType = 'emissions'
    chartColor = '#9F9A93'
    perYear = True
    weather = True

    centralCities, innerCities, outerCities = getCities(request)

    chartData = []

    yearRange = []

    emissionsObjects = Emissions.objects.all().order_by('year')
    year = ''
    for object in emissionsObjects:

        if year != object.year:
            yearRange.append(object.year)
            year = object.year

        else:
            pass

    if year != '':
        start_year = year

    else:
        start_year = None

    context = {'page': page, 'chartType': chartType, 'chartColor': chartColor, 'perYear': perYear,
               'chartData': chartData,
               'centralCities': centralCities, 'innerCities': innerCities, 'outerCities': outerCities,
               'yearRange': yearRange, 'weather': weather, 'start_year': start_year}
    setDetailContext(context)

    return render_to_response('charts/emissions.html', context)


def viewCostChart(request, page):
    chartType = 'cost'
    chartColor = '#59614B'
    perYear = True

    centralCities, innerCities, outerCities = getCities(request)

    chartData = []

    yearRange = []

    costObjects = Cost.objects.all().order_by('year')
    year = ''
    for object in costObjects:

        if year != object.year:
            yearRange.append(object.year)
            year = object.year

        else:
            pass

    if year != '':
        start_year = year

    else:
        start_year = None

    context = {'page': page, 'chartType': chartType, 'chartColor': chartColor, 'perYear': perYear,
               'chartData': chartData,
               'centralCities': centralCities, 'innerCities': innerCities, 'outerCities': outerCities,
               'yearRange': yearRange, 'start_year': start_year}
    setDetailContext(context)

    return render_to_response('charts/cost.html', context)


def getCities(request):
    try:
        centralCities = City.objects.filter(type='C')

    except Exception, e:
        print e
        centralCities = None

    try:
        innerCities = City.objects.filter(type='I')

    except Exception, e:
        print e
        innerCities = None

    try:
        outerCities = City.objects.filter(type='O')

    except Exception, e:
        print e
        outerCities = None

    return centralCities, innerCities, outerCities