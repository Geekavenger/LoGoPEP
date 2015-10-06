from city_metrics.models import Energy, City, DemographicData, SpecialTrendLine, Water, Travel, Waste, Emissions, Cost
import simplejson as json
from django.http import HttpResponse


def update_chart(request):
    json_data = {}
    chart_type = None
    chart_error = False
    all_cities = False
    city_list = []
    city_type_list = []
    year = ''
    normalize = None
    weather_norm = None
    series_data = None
    average_term = None
    col_len = None
    v_axis_label = ''
    v_axis_format = '#,###.##'
    formatter_length = 0
    error_message = None

    try:
        check_string = request.GET['aList']
    except Exception, e:
        chart_error = e
        check_string = None

    if not chart_error:
        stripped_string = check_string.strip()
        new_list = stripped_string.split(",")

        chart_type = request.GET['chartType']

        chart_data = []
        average_term = None
        stats = None
        indicator = None
        unit = None

        for item in new_list:

            if item.startswith('ind_'):
                term = item.replace('ind_', '')

                indicator = term

            if item.startswith('unit_'):
                term = item.replace('unit_', '')

                unit = term

            if item == 'All Central Cities' or item == 'All Inner Suburbs' or item == 'All Outer Suburbs':

                city_type_list.append(item)

                pass

            else:

                if item.startswith('city_'):
                    cityID = item.replace('city_', '')

                    if cityID == 'all':
                        all_cities = True
                        cities = City.objects.all()
                    else:
                        cities = City.objects.filter(id=cityID)

                    for city in cities:
                        city_list.append(city)

            if item.startswith('time_'):
                year = item.replace('time_', '')

            if item.startswith('norm_'):
                normalize = item.replace('norm_', '')

            if item.startswith('weather'):
                weather_norm = item.replace('_norm', '')

            if item.startswith('average_'):
                average_term = item.replace('average_', '')

        chart_titles = get_chart_titles(indicator, unit, average_term, year, city_list)

        chart_data.append(chart_titles)

        if unit == 'btu':
            stats = Energy.objects.all().order_by('city__sort_order')
            if normalize != 'none':
                v_axis_label = 'kBtu'
            else:
                v_axis_label = 'MMBtu'
            v_axis_format = '#,###.##'

        elif unit == 'gallons':
            stats = Water.objects.all().order_by('city__sort_order')
            v_axis_label = 'Gallons'
            v_axis_format = '#,###.##'

        elif unit == 'vmt':
            stats = Travel.objects.all().order_by('city__sort_order')
            v_axis_label = 'VMT'
            v_axis_format = '#,###.##'

        elif unit == 'tons':
            stats = Waste.objects.all().order_by('city__sort_order')
            if normalize != 'none':
                v_axis_label = 'POUNDS'
            else:
                v_axis_label = 'TONS'
            v_axis_format = '#,###.##'

        elif unit == 'co':
            stats = Emissions.objects.all().order_by('city__sort_order')
            v_axis_label = 'TONNES CO2e'
            v_axis_format = '#,###.##'

        elif unit == 'dollars':
            stats = Cost.objects.all().order_by('city__sort_order')
            v_axis_label = 'Dollars'
            v_axis_format = '$#,###.##'

        elif chart_type == 'emissions':
            stats = Emissions.objects.all().order_by('city__sort_order')
            v_axis_label = 'TONNES CO2e'
            v_axis_format = '#,###.##'

        elif chart_type == 'cost':
            stats = Cost.objects.all().order_by('city__sort_order')
            v_axis_label = 'Dollars'
            v_axis_format = '$#,###.##'

        try:

            if year == 'all':
                city_stats = stats.filter(city__in=city_list).order_by('year', 'city__sort_order')

            else:
                city_stats = stats.filter(city__in=city_list, year=year).order_by('city__sort_order', 'year')

        except Exception, e:
            print e
            city_stats = stats

        if len(city_list) > 0 and year:

            # BUILD CHART DATA
            chart_data, col_len, average, error_message = get_chart_data(chart_type, indicator, unit, chart_data, city_stats, year, normalize, weather_norm, average_term)

            # BUILD CHART SERIES
            series_data = build_series(col_len, average, year, chart_type)

        else:

            if len(city_list) == 0:
                error_message = '<h3 id="noAverageMessage">You do not have any cities chosen.</h3>'

            if not year:
                error_message = '<h3 id="noAverageMessage">You do not have a year chosen.</h3>'

            if (len(city_list) == 0) and (not year):
                error_message = '<h3 id="noAverageMessage">You do not have any cities or a year chosen.</h3>'

            chart_data = [
                ['Year', ''],
                ['none', 0],
            ]

    else:
        chart_data = [
            ['Year', ''],
            ['none', 0],
        ]

    if col_len:
        if average_term:
            if year == 'all':
                formatter_length = col_len - 1
            else:
                formatter_length = col_len + 1

        else:
            formatter_length = col_len - 1

    json_data['columns'] = chart_data
    json_data['seriesData'] = series_data
    json_data['colLen'] = formatter_length
    json_data['vAxisLabel'] = v_axis_label
    json_data['vAxisFormat'] = v_axis_format
    json_data['errorMessage'] = error_message

    # #### BUILD SUBTITLES #####
    sub_title_cities = []
    if len(city_list) > 0:

        if all_cities:

            city_string = 'All Cities'

            sub_title_cities.append(city_string)

        else:

            for city in city_list:
                city_string = ' ' + str(city.city)

                sub_title_cities.append(city_string)

    json_data['cities'] = sub_title_cities

    if year == 'all':

        years = 'All Years'

        json_data['years'] = years

    else:

        json_data['years'] = year

    normalize_title = None
    if normalize and normalize != 'none':

        # #### GET DAY FACTOR #####
        if (chart_type == 'emissions') or (chart_type == 'cost'):
            day_factor = 'Year'

        else:
            day_factor = 'Day'

        if normalize == 'population':
            normalize_title = ' | Per Capita/' + day_factor

        if normalize == 'household':
            normalize_title = ' | Per Household/' + day_factor

        if normalize == 'employment':
            normalize_title = ' | Per Job/' + day_factor

        json_data['normalizeTitle'] = normalize_title

    else:

        json_data['normalizeTitle'] = ''

    if weather_norm:

        weather_title = ' | Normalized by HDD/CDD'

        json_data['weatherTitle'] = weather_title

    else:

        json_data['weatherTitle'] = ''

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def get_chart_titles(indicator, unit, average_term, year, city_list):
    try:

        chart_titles = []

        if year == 'all':

            chart_titles.append('year')

            for city in city_list:
                name = city.city
                chart_titles.append(name)

        else:

            chart_titles.append('city')

            if (indicator == 'Total Energy by Source') or (indicator == 'Total Water by End Use Type'):
                chart_titles.append('RESIDENTIAL')
                chart_titles.append('COMMERCIAL/INDUSTRIAL')

            elif indicator == 'Total Energy by Type':
                chart_titles.append('ELECTRICITY')
                chart_titles.append('NATURAL GAS')
                chart_titles.append('OTHER')

            elif indicator == 'Total Municipal Solid Waste by Management Method':
                chart_titles.append('RECYCLED')
                chart_titles.append('LANDFILLED')
                chart_titles.append('INCINERATED')

            else:
                chart_titles.append(indicator)

        title = None
        if average_term:

            if average_term == 'A':
                title = 'RII Cities Average'

            elif average_term == 'C':
                title = 'Central/Stand Alone Cities'

            elif average_term == 'I':
                title = 'Inner-Ring Suburbs'

            elif average_term == 'O':
                title = 'Outer-Ring Suburbs'

            else:
                title = average_term

        if title:
            chart_titles.append(title)

    except Exception, e:
        print e
        chart_titles = ['year', 'stat']

    return chart_titles


def get_chart_data(chart_type, indicator, unit, chart_data, city_stats, year, normalize, weather_norm, average_term):
    chart_stat_col = []
    col_len = 0
    error_message = None

    # #### GET SCALE AND DAY FACTORS #####
    if chart_type == 'energy':
        scale_factor = 1000
        day_factor = 365

    elif chart_type == 'waste':
        scale_factor = 2000
        day_factor = 365

    elif chart_type == 'emissions':
        scale_factor = 1
        day_factor = 1

    elif chart_type == 'cost':
        scale_factor = 1
        day_factor = 1

    else:
        scale_factor = 1
        day_factor = 365

    ##### IF AVERAGE TERM, CALCULATE AVERAGE #####
    average = None
    if average_term:
        average, error_message = get_average(chart_type, indicator, unit, average_term, year, normalize, scale_factor, day_factor, weather_norm)

    statistics = None
    current_year = None
    for stat in city_stats:

        if year == 'all':
            stat_year = stat.year

            ##### GET STATISTIC #####
            statistics = get_statistic(indicator, unit, stat, weather_norm)

            if len(chart_stat_col) < 1:
                chart_stat_col.append(stat_year)

            ##### IF NORMALIZE, NORMALIZE DATA BEFORE APPENDING #####
            if normalize and normalize != 'none':
                statistics = adjust_for_normalize(normalize, stat, statistics, scale_factor, day_factor)

            ##### DETERMINE TO APPEND #####
            if (not current_year) or (current_year == stat_year):

                for statistic in statistics:
                    chart_stat_col.append(float(statistic))

                current_year = stat_year

            else:
                ##### IF AVERAGE, APPEND IT TO THE COL #####
                if not average == None:
                    chart_stat_col.append(float(average))

                chart_data.append(chart_stat_col)
                current_year = stat_year

                chart_stat_col = [stat_year]
                for statistic in statistics:
                    chart_stat_col.append(float(statistic))

            col_len = len(chart_stat_col)

        else:
            ##### GET STATISTIC #####
            statistics = get_statistic(indicator, unit, stat, weather_norm)

            city = stat.city.city

            if len(chart_stat_col) < 1:
                chart_stat_col.append(str(city))

            ##### IF NORMALIZE, NORMALIZE DATA BEFORE APPENDING #####
            if normalize and normalize != 'none':
                statistics = adjust_for_normalize(normalize, stat, statistics, scale_factor, day_factor)

            for statistic in statistics:
                chart_stat_col.append(float(statistic))

            ##### IF AVERAGE, APPEND IT TO THE COL #####
            if not average == None:
                chart_stat_col.append(float(average))

            chart_data.append(chart_stat_col)

            ##### GET COLUMN LENGTH #####
            if not average == None:
                col_len = len(chart_stat_col) - 2

            else:
                col_len = len(chart_stat_col)

            chart_stat_col = []

    if year == 'all':
        ##### IF AVERAGE, APPEND IT TO THE COL #####
        if not average == None:
            chart_stat_col.append(float(average))

        chart_data.append(chart_stat_col)

    return chart_data, col_len, average, error_message


def get_statistic(indicator, unit, stat, weather_norm):
    statistics = []
    statistic = None

    # ######### ENERGY ##########
    if indicator == 'Total Energy':
        if unit == 'btu':
            if weather_norm:
                total_energy = stat.wn_electricity + stat.wn_natural_gas + stat.wn_other
            else:
                total_energy = stat.electricity + stat.natural_gas + stat.other
        elif unit == 'co':
            if weather_norm:
                total_energy = stat.wn_energy_associated_emissions
            else:
                total_energy = stat.energy_associated_emissions
        elif unit == 'dollars':
            if weather_norm:
                total_energy = stat.wn_energy_associated_costs
            else:
                total_energy = stat.energy_associated_costs

        else:
            total_energy = None

        statistics.append(total_energy)

    elif indicator == 'Total Energy by Source':
        if unit == 'btu':
            if weather_norm:
                res_energy = stat.wn_total_res_energy
                com_energy = stat.wn_total_com_ind_energy
            else:
                res_energy = stat.total_res_energy
                com_energy = stat.total_com_ind_energy
        elif unit == 'co':
            if weather_norm:
                res_energy = stat.wn_energy_use_residential
                com_energy = stat.wn_energy_use_com_ind
            else:
                res_energy = stat.energy_use_residential
                com_energy = stat.energy_use_com_ind
        elif unit == 'dollars':
            if weather_norm:
                res_energy = stat.wn_energy_use_residential
                com_energy = stat.wn_energy_use_com_ind
            else:
                res_energy = stat.energy_use_residential
                com_energy = stat.energy_use_com_ind

        else:
            res_energy = 0
            com_energy = 0

        if not res_energy or not com_energy:
            res_energy = 0
            com_energy = 0

        statistics.append(res_energy)
        statistics.append(com_energy)

    elif indicator == 'Total Energy by Type':
        if unit == 'btu':
            if weather_norm:
                electricity = stat.wn_electricity
                gas = stat.wn_natural_gas
                other = stat.wn_other
            else:
                electricity = stat.electricity
                gas = stat.natural_gas
                other = stat.other
        elif unit == 'co':
            if weather_norm:
                electricity = stat.wn_energy_type_electricity
                gas = stat.wn_energy_type_natural_gas
                other = stat.wn_energy_type_other
            else:
                electricity = stat.energy_type_electricity
                gas = stat.energy_type_natural_gas
                other = stat.energy_type_other
        elif unit == 'dollars':
            if weather_norm:
                electricity = stat.wn_energy_type_electricity
                gas = stat.wn_energy_type_natural_gas
                other = stat.wn_energy_type_other
            else:
                electricity = stat.energy_type_electricity
                gas = stat.energy_type_natural_gas
                other = stat.energy_type_other

        else:
            electricity = None
            gas = None
            other = None

        statistics.append(electricity)
        statistics.append(gas)
        statistics.append(other)

    elif indicator == 'Residential Energy':
        if unit == 'btu':
            if weather_norm:
                res_energy = stat.wn_total_res_energy
            else:
                res_energy = stat.total_res_energy
        elif unit == 'co':
            if weather_norm:
                res_energy = stat.wn_energy_use_residential
            else:
                res_energy = stat.energy_use_residential
        elif unit == 'dollars':
            if weather_norm:
                res_energy = stat.wn_energy_use_residential
            else:
                res_energy = stat.energy_use_residential

        else:
            res_energy = None

        statistics.append(res_energy)

    elif indicator == 'Commercial/Industrial Energy':
        if unit == 'btu':
            if weather_norm:
                com_energy = stat.wn_total_com_ind_energy
            else:
                com_energy = stat.total_com_ind_energy
        elif unit == 'co':
            if weather_norm:
                com_energy = stat.wn_energy_use_com_ind
            else:
                com_energy = stat.energy_use_com_ind
        elif unit == 'dollars':
            if weather_norm:
                com_energy = stat.wn_energy_use_com_ind
            else:
                com_energy = stat.energy_use_com_ind

        else:
            com_energy = None

        statistics.append(com_energy)

    ########## WATER ##########
    elif indicator == 'Total Water':
        if unit == 'gallons':
            total_water = stat.total_res_water + stat.total_com_ind_water
        elif unit == 'dollars':
            total_water = stat.water_associated_costs

        else:
            total_water = None

        statistics.append(total_water)

    elif indicator == 'Total Water by End Use Type':
        if unit == 'gallons':
            res_water = stat.total_res_water
            com_water = stat.total_com_ind_water
        elif unit == 'dollars':
            res_water = stat.water_use_residential
            com_water = stat.water_use_com_ind

        else:
            res_water = None
            com_water = None

        statistics.append(res_water)
        statistics.append(com_water)

    elif indicator == 'Residential Water':
        if unit == 'gallons':
            statistic = stat.total_res_water
        if unit == 'dollars':
            statistic = stat.water_use_residential

    elif indicator == 'Commercial/Industrial Water':
        if unit == 'gallons':
            statistic = stat.total_com_ind_water
        if unit == 'dollars':
            statistic = stat.water_use_com_ind

    ########## TRAVEL ##########
    elif indicator == 'Total VMT':
        if unit == 'vmt':
            total_stat = stat.total_vmt
        elif unit == 'co':
            if weather_norm:
                total_stat = stat.wn_travel_associated_emissions
            else:
                total_stat = stat.travel_associated_emissions
        elif unit == 'dollars':
            total_stat = stat.travel_associated_costs

        else:
            total_stat = None

        statistics.append(total_stat)

    ########## WASTE ##########
    elif indicator == 'Total Municipal Solid Waste':
        if unit == 'tons':
            total_stat = stat.recycled + stat.landfilled + stat.incinerated
        elif unit == 'co':
            total_stat = stat.waste_associated_emissions
        elif unit == 'dollars':
            total_stat = stat.waste_associated_costs

        else:
            total_stat = None

        statistics.append(total_stat)

    elif indicator == 'Total Municipal Solid Waste by Management Method':
        if unit == 'tons':
            recycled = stat.recycled
            land_filled = stat.landfilled
            incinerated = stat.incinerated
        elif unit == 'co' or unit == 'dollars':
            recycled = stat.waste_method_recycled
            land_filled = stat.waste_method_landfilled
            incinerated = stat.waste_method_incinerated

        else:
            recycled = None
            land_filled = None
            incinerated = None

        statistics.append(recycled)
        statistics.append(land_filled)
        statistics.append(incinerated)

    ########## EMISSIONS ##########
    elif indicator == 'Total GHG Emissions':

        if weather_norm:
            total_emissions = stat.wn_energy_associated_emissions + stat.wn_water_associated_emissions + stat.wn_travel_associated_emissions + stat.wn_waste_associated_emissions
        else:
            total_emissions = stat.energy_associated_emissions + stat.water_associated_emissions + stat.travel_associated_emissions + stat.waste_associated_emissions

        statistics.append(total_emissions)

    elif indicator == 'Energy-Associated GHG Emissions':

        if weather_norm:
            energy_emissions = stat.wn_energy_associated_emissions
        else:
            energy_emissions = stat.energy_associated_emissions
        statistics.append(energy_emissions)

    elif indicator == 'Other GHG Emissions':

        if weather_norm:
            water_emissions = stat.wn_water_associated_emissions
        else:
            water_emissions = stat.water_associated_emissions
        statistics.append(water_emissions)

    elif indicator == 'Travel-Associated GHG Emissions':

        if weather_norm:
            travel_emissions = stat.wn_travel_associated_emissions
        else:
            travel_emissions = stat.travel_associated_emissions
        statistics.append(travel_emissions)

    elif indicator == 'Waste-Associated GHG Emissions':

        if weather_norm:
            waste_emissions = stat.wn_waste_associated_emissions
        else:
            waste_emissions = stat.waste_associated_emissions
        statistics.append(waste_emissions)

    ########## COST ##########
    elif indicator == 'Total Costs':
        total_costs = stat.energy_associated_costs + stat.water_associated_costs + stat.travel_associated_costs + stat.waste_associated_costs

        statistics.append(total_costs)

    elif indicator == 'Energy-Associated Costs':
        energy_costs = stat.energy_associated_costs
        statistics.append(energy_costs)

    elif indicator == 'Water-Associated Costs':
        water_costs = stat.water_associated_costs
        statistics.append(water_costs)

    elif indicator == 'Travel-Associated Costs':
        travel_costs = stat.travel_associated_costs
        statistics.append(travel_costs)

    elif indicator == 'Waste-Associated Costs':
        waste_costs = stat.waste_associated_costs
        statistics.append(waste_costs)

    ########## APPEND STATISTIC ##########
    if not statistic == None:
        statistics.append(statistic)

    return statistics


def adjust_for_normalize(normalize, stat, statistics, scale_factor, day_factor):
    year = stat.year
    city = stat.city
    data = None
    norm_statistics = []

    try:
        demographic_data = DemographicData.objects.get(city=city, year=year)

    except Exception, e:
        print e
        demographic_data = None

    if demographic_data:

        if normalize == 'population':
            data = demographic_data.population

        if normalize == 'household':
            data = demographic_data.households

        if normalize == 'employment':
            data = demographic_data.jobs

    if data:

        for statistic in statistics:
            norm_statistic = statistic / data / day_factor * scale_factor
            norm_statistics.append(norm_statistic)

    return norm_statistics


def get_average(chart_type, indicator, unit, average_term, year, normalize, scale_factor, day_factor, weather_norm):
    all_years = None
    objects = None
    average_sum = 0
    statistic_sum = 0
    count = 0
    stats = None
    average = None
    error_message = None

    # #### IF ALL YEARS SELECTED SET VARIABLE #####
    if year == 'all':
        all_years = True

    ##### DETERMINE OBJECTS TO AVERAGE #####
    chart_stats = None
    if unit == 'btu':
        chart_stats = 'energy'
        objects = Energy.objects.all()

    elif unit == 'gallons':
        chart_stats = 'water'
        objects = Water.objects.all()

    elif unit == 'vmt':
        chart_stats = 'travel'
        objects = Travel.objects.all()

    elif unit == 'tons':
        chart_stats = 'waste'
        objects = Waste.objects.all()

    elif unit == 'co' or chart_type == 'emissions':
        chart_stats = 'emissions'
        objects = Emissions.objects.all()

    elif unit == 'dollars' or chart_type == 'cost':
        chart_stats = 'cost'
        objects = Cost.objects.all()

    ##### FIND AVERAGE #####
    if average_term == 'A':
        if all_years:
            stats = objects
        else:
            stats = objects.filter(year=year)

    elif average_term == 'State' or average_term == 'US':

        try:

            if all_years:
                special_averages = SpecialTrendLine.objects.filter(type=average_term, chart=chart_stats)

            else:
                special_averages = SpecialTrendLine.objects.filter(type=average_term, chart=chart_stats, year=year)

            for specialAverage in special_averages:

                average = specialAverage.no_normalize

                ##### NORMALIZE DATA BEFORE APPENDING #####
                if normalize == 'population':
                    average = specialAverage.capita_normalize

                if normalize == 'household':
                    average = specialAverage.household_normalize

                if normalize == 'employment':
                    average = specialAverage.employment_normalize

                average_sum += average
                count += 1

            average = average_sum / count

        except Exception, e:
            print e
            average = 0
            error_message = '<h3 id="noAverageMessage">Sorry, we do not currently have the ' + average_term + ' Average for ' + year + '.</h3>'

    else:
        if all_years:
            stats = objects.filter(city__type=average_term)
        else:
            stats = objects.filter(city__type=average_term, year=year)

    if stats:

        count = 0
        for stat in stats:

            statistics = get_statistic(indicator, unit, stat, weather_norm)
            norm_statistics = None

            statistic = 0
            ##### IF NORMALIZE, NORMALIZE DATA BEFORE APPENDING #####
            if normalize and normalize != 'none':
                norm_statistics = adjust_for_normalize(normalize, stat, statistics, scale_factor, day_factor)

                for item in norm_statistics:
                    statistic += item

            else:

                for item in statistics:
                    statistic += item

            statistic_sum += statistic
            count += 1

        average = statistic_sum / count

    return average, error_message


def build_series(colLen, average, year, chartType):
    color = 'color'
    type = 'type'

    bar_color_options, line_color_options = color_codes(chartType)

    series_data = {}

    position = 0
    for i in range(0, colLen):
        if year == 'all':
            series_data[i] = {type: "line", color: line_color_options[i]}

        else:
            series_data[i] = {color: bar_color_options[i]}

        position += 1

    if not average == None:
        series_data[position] = {type: "line", color: line_color_options[0], "pointSize": "5"}

    return series_data


def color_codes(chart_type):
    bar_color_options = []
    line_color_options = []

    if chart_type == 'energy':
        bar_color_options = ['#F18C39', '#F8B417', '#FDD301', '#FDE930']
        line_color_options = ['#71161a', '#b24034', '#b35d2c', '#8c4b20', '#815c24', '#967731', '#b19c45', '#c02426',
                              '#f16243', '#e67a46', '#f18c39', '#f8b417', '#fdd301', '#fde930', '#d37982', '#ea938c',
                              '#f2bea3', '#f1ad78', '#f7cc76', '#fbe68f', '#fef4b4', '#fef4b4', '#fef4b4']

    elif chart_type == 'water':
        bar_color_options = ['#8DC6EB', '#969FD0', '#8B61A1', '#BC559F']
        line_color_options = ['#5b2a4f', '#4b3658', '#4b5166', '#4c6b7c', '#225260', '#1b6266', '#195e3b', '#bc559f',
                              '#8b61a1', '#969fd0', '#8dc6eb', '#41a4d0', '#2ca3af', '#2bb174', '#d094c1', '#b095c0',
                              '#bbc0e1', '#bfdbee', '#a7d2dc', '#7fbfc5', '#8ecaa5', '#8ecaa5', '#8ecaa5']

    elif chart_type == 'travel':
        bar_color_options = ['#96C94D', '#6cbd44', '#2bb174', '#2ca3af']
        line_color_options = ['#1b6266', '#195e3b', '#3a602d', '#52682f', '#6a7531', '#818233', '#b19c45', '#2ca3af',
                              '#2bb174', '#6cbd44', '#96c94d', '#b5cf33', '#dde230', '#fde930', '#7fbfc5', '#8ecaa5',
                              '#a0c18b', '#bedb89', '#d0df87', '#e9eb8d', '#fef4b4', '#fef4b4', '#fef4b4']

    elif chart_type == 'waste':
        bar_color_options = ['#8B61A1', '#BC559F', '#D094C1', '#B095C0']
        line_color_options = ['#5b2a4f', '#4b3658', '#4b5166', '#4c6b7c', '#225260', '#bc559f', '#8b61a1', '#969fd0',
                              '#8dc6eb', '#41a4d0', '#d094c1', '#b095c0', '#bbc0e1', '#bfdbee', '#a7d2dc', '#c5746a',
                              '#d37982', '#9b1c34', '#c02426', '#4d1322', '#71161a', '#71161a', '#71161a']

    elif chart_type == 'emissions':
        bar_color_options = ['#9F9A93', '#627177', '#555966', '#4E4754']
        line_color_options = ['#627177', '#555966', '#4E4754', '#564253', '#3d303b', '#483a3e', '#6d5c5e', '#ae7874',
                              '#b1826a', '#896652', '#7f6c52', '#938261', '#aea270', '#7e7f54', '#6e7250', '#5a6644',
                              '#4d5b47', '#4a564f', '#4d6665', '#47585b', '#627177', '#627177', '#627177']

    elif chart_type == 'cost':
        bar_color_options = ['#59614B', '#447676', '#427787', '#627577']
        line_color_options = ['#447676', '#427787', '#627577', '#556166', '#4e4854', '#565153', '#3d3c3b', '#48463e',
                              '#6d685e', '#ac8b72', '#af9768', '#888950', '#7f9150', '#92a860', '#aeba70', '#9bb56d',
                              '#7a9857', '#699050', '#4c7747', '#426046', '#447676', '#447676', '#447676']

    return bar_color_options, line_color_options