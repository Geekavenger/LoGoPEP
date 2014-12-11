import string
from django.shortcuts import render_to_response
from django.template import RequestContext
from city_metrics.models import Energy, City, DemographicData, Water, Travel, Waste, Emissions, Cost
from csvParser import CSVParser


allchars = string.maketrans('', '')


def makefilter(keep):
    delchars = allchars.translate(allchars, keep)

    def thefilter(s):
        return s.translate(allchars, delchars)

    return thefilter


stringFilter = makefilter(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890()-=,.;:/\\[]{}!@#$%^&*~<>? \"\'')


def demographicDataImporter(request):
    errorMessage = None
    updateCount = 0
    newCount = 0
    errorCount = 0
    rowCount = 0

    if request.method == 'POST':
        file_obj = request.FILES['file']

        if file_obj:
            import StringIO

            buf = StringIO.StringIO(file_obj.read())

            parser = CSVParser().parse

            updateCount = 0
            newCount = 0
            errorCount = 0
            rowCount = 0
            errorLines = list()

            for row in buf:
                rowCount += 1

                filteredRow = stringFilter(row)

                fields = parser(filteredRow)

                if None == fields:
                    continue

                if len(fields) < 5:
                    continue

                city = fields[0]
                year = fields[1]

                if fields[2]:
                    population = fields[2].replace(",", "")
                else:
                    population = 0

                if fields[3]:
                    jobs = fields[3].replace(",", "")
                else:
                    jobs = 0

                if fields[4]:
                    households = fields[4].replace(",", "")
                else:
                    households = 0

                if city == 'City':
                    continue

                try:

                    # # Find City ##
                    cityObject = City.objects.get(city=city)

                    newItem = DemographicData()
                    newItem.city = cityObject
                    newItem.year = year
                    newItem.population = population
                    newItem.jobs = jobs
                    newItem.households = households
                    newItem.save()

                    print 'committing row ' + row

                except Exception, e:
                    print e
                    errorMessage = 'There was an error uploading the item on row ' + str(
                        rowCount) + ', please fix before continuing.'
                    pass

    else:
        pass

    context = {'errorMessage': errorMessage, 'message': 'Successful', 'updateCount': updateCount, 'newCount': newCount,
               'errorCount': errorCount}

    return render_to_response('admin_imports/demographic_data_importer.html', context,
                              context_instance=RequestContext(request))


def energyImporter(request):
    errorMessage = None
    updateCount = 0
    newCount = 0
    errorCount = 0
    rowCount = 0

    if request.method == 'POST':
        file_obj = request.FILES['file']

        if file_obj:
            import StringIO

            buf = StringIO.StringIO(file_obj.read())

            parser = CSVParser().parse

            updateCount = 0
            newCount = 0
            errorCount = 0
            rowCount = 0
            errorLines = list()

            for row in buf:
                rowCount += 1

                filteredRow = stringFilter(row)

                fields = parser(filteredRow)

                if None == fields:
                    continue

                if len(fields) < 12:
                    continue

                city = fields[0]
                year = fields[1]

                # WN = WEATHER NORMALIZED
                # TYPES
                electricity = fields[2].replace(",", "")
                natural_gas = fields[3].replace(",", "")
                other = fields[4].replace(",", "")

                # WN TYPE
                wn_electricity = fields[5].replace(",", "")
                wn_natural_gas = fields[6].replace(",", "")
                wn_other = fields[7].replace(",", "")

                # TOTALS BY USE
                total_res_energy = fields[8].replace(",", "")
                total_com_ind_energy = fields[9].replace(",", "")

                # WN TOTALS BY USE
                wn_total_res_energy = fields[10].replace(",", "")
                wn_total_com_ind_energy = fields[11].replace(",", "")

                if city == 'City':
                    continue

                try:

                    # Find City
                    cityObject = City.objects.get(city=city)

                    newItem = Energy()
                    newItem.city = cityObject
                    newItem.year = year
                    newItem.electricity = electricity
                    newItem.natural_gas = natural_gas
                    newItem.other = other
                    newItem.wn_electricity = wn_electricity
                    newItem.wn_natural_gas = wn_natural_gas
                    newItem.wn_other = wn_other
                    newItem.total_res_energy = total_res_energy
                    newItem.total_com_ind_energy = total_com_ind_energy
                    newItem.wn_total_res_energy = wn_total_res_energy
                    newItem.wn_total_com_ind_energy = wn_total_com_ind_energy
                    newItem.save()

                    print 'committing row ' + row

                except Exception, e:
                    print e
                    errorMessage = 'There was an error uploading the item on row ' + str(
                        rowCount) + ', please fix before continuing.'
                    pass

    else:
        pass

    context = {'errorMessage': errorMessage, 'message': 'Successful', 'updateCount': updateCount, 'newCount': newCount,
               'errorCount': errorCount, }

    return render_to_response('admin_imports/energy_importer.html', context, context_instance=RequestContext(request))


def waterImporter(request):
    errorMessage = None
    updateCount = 0
    newCount = 0
    errorCount = 0
    rowCount = 0

    if request.method == 'POST':
        file_obj = request.FILES['file']

        if file_obj:
            import StringIO

            buf = StringIO.StringIO(file_obj.read())

            parser = CSVParser().parse

            updateCount = 0
            newCount = 0
            errorCount = 0
            rowCount = 0
            errorLines = list()

            for row in buf:
                rowCount += 1

                filteredRow = stringFilter(row)

                fields = parser(filteredRow)

                if None == fields:
                    continue

                if len(fields) < 4:
                    continue

                city = fields[0]
                year = fields[1]

                total_res_water = fields[2].replace(",", "")
                total_com_ind_water = fields[3].replace(",", "")

                if city == 'City':
                    continue

                try:

                    # # Find City ##
                    cityObject = City.objects.get(city=city)

                    newItem = Water()
                    newItem.city = cityObject
                    newItem.year = year
                    newItem.total_res_water = total_res_water
                    newItem.total_com_ind_water = total_com_ind_water
                    newItem.save()

                    print 'committing row ' + row

                except Exception, e:
                    print e
                    errorMessage = 'There was an error uploading the item on row ' + str(
                        rowCount) + ', please fix before continuing.'
                    pass

    else:
        pass

    context = {'errorMessage': errorMessage, 'message': 'Successful', 'updateCount': updateCount, 'newCount': newCount,
               'errorCount': errorCount, }

    return render_to_response('admin_imports/water_importer.html', context, context_instance=RequestContext(request))


def travelImporter(request):
    errorMessage = None
    updateCount = 0
    newCount = 0
    errorCount = 0
    rowCount = 0

    if request.method == 'POST':
        file_obj = request.FILES['file']

        if file_obj:
            import StringIO

            buf = StringIO.StringIO(file_obj.read())

            parser = CSVParser().parse

            updateCount = 0
            newCount = 0
            errorCount = 0
            rowCount = 0
            errorLines = list()

            for row in buf:
                rowCount += 1

                filteredRow = stringFilter(row)

                fields = parser(filteredRow)

                if None == fields:
                    continue

                if len(fields) < 3:
                    continue

                city = fields[0]
                year = fields[1]

                total_vmt = fields[2].replace(",", "")

                if city == 'City':
                    continue

                try:

                    # # Find City ##
                    cityObject = City.objects.get(city=city)

                    newItem = Travel()
                    newItem.city = cityObject
                    newItem.year = year
                    newItem.total_vmt = total_vmt
                    newItem.save()

                    print 'committing row ' + row

                except Exception, e:
                    print e
                    errorMessage = 'There was an error uploading the item on row ' + str(
                        rowCount) + ', please fix before continuing.'
                    pass

    else:
        pass

    context = {'errorMessage': errorMessage, 'message': 'Successful', 'updateCount': updateCount, 'newCount': newCount,
               'errorCount': errorCount, }

    return render_to_response('admin_imports/travel_importer.html', context, context_instance=RequestContext(request))


def wasteImporter(request):
    errorMessage = None
    updateCount = 0
    newCount = 0
    errorCount = 0
    rowCount = 0

    if request.method == 'POST':
        file_obj = request.FILES['file']

        if file_obj:
            import StringIO

            buf = StringIO.StringIO(file_obj.read())

            parser = CSVParser().parse

            updateCount = 0
            newCount = 0
            errorCount = 0
            rowCount = 0
            errorLines = list()

            for row in buf:
                rowCount += 1

                filteredRow = stringFilter(row)

                fields = parser(filteredRow)

                if None == fields:
                    continue

                if len(fields) < 5:
                    continue

                city = fields[0]
                year = fields[1]

                recycled = fields[2].replace(",", "")
                landfilled = fields[3].replace(",", "")
                incinerated = fields[4].replace(",", "")

                if city == 'City':
                    continue

                try:

                    # # Find City ##
                    cityObject = City.objects.get(city=city)

                    newItem = Waste()
                    newItem.city = cityObject
                    newItem.year = year
                    newItem.recycled = recycled
                    newItem.landfilled = landfilled
                    newItem.incinerated = incinerated
                    newItem.save()

                    print 'committing row ' + row

                except Exception, e:
                    print e
                    errorMessage = 'There was an error uploading the item on row ' + str(
                        rowCount) + ', please fix before continuing.'
                    pass

    else:
        pass

    context = {'errorMessage': errorMessage, 'message': 'Successful', 'updateCount': updateCount, 'newCount': newCount,
               'errorCount': errorCount, }

    return render_to_response('admin_imports/waste_importer.html', context, context_instance=RequestContext(request))


def emissionsImporter(request):
    errorMessage = None
    updateCount = 0
    newCount = 0
    errorCount = 0
    rowCount = 0

    if request.method == 'POST':
        file_obj = request.FILES['file']

        if file_obj:
            import StringIO

            buf = StringIO.StringIO(file_obj.read())

            parser = CSVParser().parse

            updateCount = 0
            newCount = 0
            errorCount = 0
            rowCount = 0
            errorLines = list()

            for row in buf:
                rowCount += 1

                filteredRow = stringFilter(row)

                fields = parser(filteredRow)

                if None == fields:
                    continue

                if len(fields) < 23:
                    continue

                city = fields[0]
                year = fields[1]

                # TOTALS BY TYPE
                energy_associated_emissions = fields[2].replace(",", "")
                water_associated_emissions = fields[3].replace(",", "")
                travel_associated_emissions = fields[4].replace(",", "")
                waste_associated_emissions = fields[5].replace(",", "")

                # WN = WEATHER NORMALIZED
                # WN TOTALS BY TYPE
                wn_energy_associated_emissions = fields[6].replace(",", "")
                wn_water_associated_emissions = fields[7].replace(",", "")
                wn_travel_associated_emissions = fields[8].replace(",", "")
                wn_waste_associated_emissions = fields[9].replace(",", "")

                # ENERGY BY TYPE
                energy_type_electricity = fields[10].replace(",", "")
                wn_energy_type_electricity = fields[11].replace(",", "")
                energy_type_natural_gas = fields[12].replace(",", "")
                wn_energy_type_natural_gas = fields[13].replace(",", "")
                energy_type_other = fields[14].replace(",", "")
                wn_energy_type_other = fields[15].replace(",", "")

                # ENERGY BY USE
                energy_use_residential = fields[16].replace(",", "")
                wn_energy_use_residential = fields[17].replace(",", "")
                energy_use_com_ind = fields[18].replace(",", "")
                wn_energy_use_com_ind = fields[19].replace(",", "")

                # WASTE BY METHOD
                waste_method_recycled = fields[20].replace(",", "")
                waste_method_landfilled = fields[21].replace(",", "")
                waste_method_incinerated = fields[22].replace(",", "")

                if city == 'City':
                    continue

                try:

                    # # Find City ##
                    city_object = City.objects.get(city=city)

                    new_item = Emissions()
                    new_item.city = city_object
                    new_item.year = year
                    new_item.energy_associated_emissions = energy_associated_emissions
                    new_item.water_associated_emissions = water_associated_emissions
                    new_item.travel_associated_emissions = travel_associated_emissions
                    new_item.waste_associated_emissions = waste_associated_emissions
                    new_item.wn_energy_associated_emissions = wn_energy_associated_emissions
                    new_item.wn_water_associated_emissions = wn_water_associated_emissions
                    new_item.wn_travel_associated_emissions = wn_travel_associated_emissions
                    new_item.wn_waste_associated_emissions = wn_waste_associated_emissions

                    new_item.energy_type_electricity = energy_type_electricity
                    new_item.wn_energy_type_electricity = wn_energy_type_electricity
                    new_item.energy_type_natural_gas = energy_type_natural_gas
                    new_item.wn_energy_type_natural_gas = wn_energy_type_natural_gas
                    new_item.energy_type_other = energy_type_other
                    new_item.wn_energy_type_other = wn_energy_type_other
                    new_item.energy_use_residential = energy_use_residential
                    new_item.wn_energy_use_residential = wn_energy_use_residential
                    new_item.energy_use_com_ind = energy_use_com_ind
                    new_item.wn_energy_use_com_ind = wn_energy_use_com_ind
                    new_item.waste_method_recycled = waste_method_recycled
                    new_item.waste_method_landfilled = waste_method_landfilled
                    new_item.waste_method_incinerated = waste_method_incinerated
                    new_item.save()

                    print 'committing row ' + row

                except Exception, e:
                    print e
                    errorMessage = 'There was an error uploading the item on row ' + str(
                        rowCount) + ', please fix before continuing.'
                    pass

    else:
        pass

    context = {'errorMessage': errorMessage, 'message': 'Successful', 'updateCount': updateCount, 'newCount': newCount,
               'errorCount': errorCount, }

    return render_to_response('admin_imports/emissions_importer.html', context,
                              context_instance=RequestContext(request))


def costImporter(request):
    error_message = None
    update_count = 0
    new_count = 0
    error_count = 0

    if request.method == 'POST':
        file_obj = request.FILES['file']

        if file_obj:
            import StringIO

            buf = StringIO.StringIO(file_obj.read())

            parser = CSVParser().parse

            update_count = 0
            new_count = 0
            error_count = 0
            row_count = 0

            for row in buf:
                row_count += 1

                filteredRow = stringFilter(row)

                fields = parser(filteredRow)

                if None == fields:
                    continue

                if len(fields) < 22:
                    continue

                city = fields[0]
                year = fields[1]

                if city == 'City':
                    continue

                energy_associated_costs = fields[2].replace(",", "")
                wn_energy_associated_costs = fields[3].replace(",", "")
                water_associated_costs = fields[4].replace(",", "")
                travel_associated_costs = fields[5].replace(",", "")
                waste_associated_costs = fields[6].replace(",", "")

                # ENERGY BY TYPE
                energy_type_electricity = fields[7].replace(",", "")
                energy_type_natural_gas = fields[8].replace(",", "")
                energy_type_other = fields[9].replace(",", "")

                # WN ENERGY BY TYPE
                wn_energy_type_electricity = fields[10].replace(",", "")
                wn_energy_type_natural_gas = fields[11].replace(",", "")
                wn_energy_type_other = fields[12].replace(",", "")

                # ENERGY BY USE
                energy_use_residential = fields[13].replace(",", "")
                energy_use_com_ind = fields[14].replace(",", "")

                # WN ENERGY BY USE
                wn_energy_use_residential = fields[15].replace(",", "")
                wn_energy_use_com_ind = fields[16].replace(",", "")

                # WATER BY USE
                water_use_residential = fields[17].replace(",", "")
                water_use_com_ind = fields[18].replace(",", "")

                # WASTE BY METHOD
                waste_method_recycled = fields[19].replace(",", "")
                waste_method_landfilled = fields[20].replace(",", "")
                waste_method_incinerated = fields[21].replace(",", "")

                try:
                    # Find City
                    city_object = City.objects.get(city=city)

                    new_item = Cost()
                    new_item.city = city_object
                    new_item.year = year
                    new_item.energy_associated_costs = energy_associated_costs
                    new_item.wn_energy_associated_costs = wn_energy_associated_costs
                    new_item.water_associated_costs = water_associated_costs
                    new_item.travel_associated_costs = travel_associated_costs
                    new_item.waste_associated_costs = waste_associated_costs
                    new_item.energy_type_electricity = energy_type_electricity
                    new_item.energy_type_natural_gas = energy_type_natural_gas
                    new_item.energy_type_other = energy_type_other
                    new_item.wn_energy_type_electricity = wn_energy_type_electricity
                    new_item.wn_energy_type_natural_gas = wn_energy_type_natural_gas
                    new_item.wn_energy_type_other = wn_energy_type_other
                    new_item.energy_use_residential = energy_use_residential
                    new_item.energy_use_com_ind = energy_use_com_ind
                    new_item.wn_energy_use_residential = wn_energy_use_residential
                    new_item.wn_energy_use_com_ind = wn_energy_use_com_ind
                    new_item.water_use_residential = water_use_residential
                    new_item.water_use_com_ind = water_use_com_ind
                    new_item.waste_method_recycled = waste_method_recycled
                    new_item.waste_method_landfilled = waste_method_landfilled
                    new_item.waste_method_incinerated = waste_method_incinerated
                    new_item.save()

                    print 'committing row ' + row

                except Exception, e:
                    print e
                    error_message = 'There was an error uploading the item on row ' + str(row_count) + ', please fix before continuing.'
                    pass

    else:
        pass

    context = {'error_message': error_message, 'message': 'Successful', 'update_count': update_count, 'new_count': new_count,
               'error_count': error_count, }

    return render_to_response('admin_imports/cost_importer.html', context, context_instance=RequestContext(request))


allchars = string.maketrans('', '')