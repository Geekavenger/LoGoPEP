from django.db import models


CITY_TYPES = (
	('C', 'Central/Stand Alone'),
	('I', 'Inner-Ring Suburbs'),
	('O', 'Outer-Ring Suburbs'),
)


class City(models.Model):
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)

	type = models.CharField(max_length=100, choices=CITY_TYPES)

	sort_order = models.IntegerField()

	def __unicode__(self):
		return " %s, %s" % (self.city, self.state)

	class Meta:
		verbose_name = 'City'
		verbose_name_plural = 'Cities'
		ordering = ('sort_order',)


class DemographicData(models.Model):
	city = models.ForeignKey(City)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	population = models.DecimalField(max_digits=16, decimal_places=4)
	jobs = models.DecimalField(max_digits=16, decimal_places=4)
	households = models.DecimalField(max_digits=16, decimal_places=4)

	def __unicode__(self):
		return "Population - %s, %s" % (self.city.city, self.city.state)

	class Meta:
		verbose_name = 'Demographic Data'
		verbose_name_plural = 'Demographic Data'
		ordering = ('year', 'city__city')


class Energy(models.Model):
	city = models.ForeignKey(City)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	# BY TYPE
	electricity = models.DecimalField(max_digits=16, decimal_places=4)
	natural_gas = models.DecimalField(max_digits=16, decimal_places=4)
	other = models.DecimalField(max_digits=16, decimal_places=4)

	# WN BY TYPE
	# WN = Weather Normalized
	wn_electricity = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN electricity')
	wn_natural_gas = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN natural gas')
	wn_other = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN other')

	# TOTALS BY USE
	total_res_energy = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='Residential energy')
	total_com_ind_energy = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='Com/Ind energy')

	# WN TOTALS BY USE
	wn_total_res_energy = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN Residential energy')
	wn_total_com_ind_energy = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN Com/Ind energy')

	def __unicode__(self):
		return "Energy - %s, %s" % (self.city.city, self.city.state)

	class Meta:
		verbose_name = 'Energy'
		verbose_name_plural = 'Energy'


class Water(models.Model):
	city = models.ForeignKey(City)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	# TOTALS BY USE
	total_res_water = models.DecimalField(max_digits=16, decimal_places=4)
	total_com_ind_water = models.DecimalField(max_digits=16, decimal_places=4)

	def __unicode__(self):
		return "Water - %s, %s" % (self.city.city, self.city.state)

	class Meta:
		verbose_name = 'Water'
		verbose_name_plural = 'Water'


class Travel(models.Model):
	city = models.ForeignKey(City)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	total_vmt = models.DecimalField(max_digits=16, decimal_places=4)

	def __unicode__(self):
		return "Travel - %s, %s" % (self.city.city, self.city.state)

	class Meta:
		verbose_name = 'Travel'
		verbose_name_plural = 'Travel'


class Waste(models.Model):
	city = models.ForeignKey(City)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	recycled = models.DecimalField(max_digits=16, decimal_places=4)
	landfilled = models.DecimalField(max_digits=16, decimal_places=4)
	incinerated = models.DecimalField(max_digits=16, decimal_places=4)

	def __unicode__(self):
		return "Waste - %s, %s" % (self.city.city, self.city.state)

	class Meta:
		verbose_name = 'Waste'
		verbose_name_plural = 'Waste'


class Emissions(models.Model):
	city = models.ForeignKey(City)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	# TOTALS
	energy_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='Energy emission totals')
	water_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='Other emission totals')
	travel_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='Travel emission totals')
	waste_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='Waste emission totals')

	# WN TOTALS
	wn_energy_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN Total energy emissions')
	wn_water_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN Total water emissions')
	wn_travel_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN Total travel emissions')
	wn_waste_associated_emissions = models.DecimalField(max_digits=16, decimal_places=4, verbose_name='WN Total waste emissions')

	# ENERGY BY TYPE
	energy_type_electricity = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	wn_energy_type_electricity = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy type electricity')
	energy_type_natural_gas = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	wn_energy_type_natural_gas = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy type natural gas')
	energy_type_other = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	wn_energy_type_other = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy type other')

	# ENERGY BY USE
	energy_use_residential = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	wn_energy_use_residential = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy use residential')
	energy_use_com_ind = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	wn_energy_use_com_ind = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy use com/ind')

	# WASTE BY METHOD
	waste_method_recycled = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	waste_method_landfilled = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	waste_method_incinerated = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)

	def __unicode__(self):
		return "Emissions - %s, %s" % (self.city.city, self.city.state)

	class Meta:
		verbose_name = 'Emission'
		verbose_name_plural = 'Emissions'


class Cost(models.Model):
	city = models.ForeignKey(City)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	# TOTALS
	energy_associated_costs = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='Total energy costs')
	water_associated_costs = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='Total water costs')
	travel_associated_costs = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='Total travel costs')
	waste_associated_costs = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='Total waste costs')

	# WN TOTALS
	wn_energy_associated_costs = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN total energy costs')

	# ENERGY BY TYPE
	energy_type_electricity = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	energy_type_natural_gas = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	energy_type_other = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)

	# WN ENERGY BY TYPE
	wn_energy_type_electricity = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy type electricity')
	wn_energy_type_natural_gas = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy type natural gas')
	wn_energy_type_other = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy type other')

	# ENERGY BY USE
	energy_use_residential = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	energy_use_com_ind = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='Energy use com/ind')

	# WN ENERGY BY USE
	wn_energy_use_residential = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy use residential')
	wn_energy_use_com_ind = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='WN energy use com/ind')

	# WATER BY USE
	water_use_residential = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	water_use_com_ind = models.DecimalField(max_digits=16, decimal_places=4, default=0.00, verbose_name='Water use com/ind')

	# WASTE BY METHOD
	waste_method_recycled = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	waste_method_landfilled = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)
	waste_method_incinerated = models.DecimalField(max_digits=16, decimal_places=4, default=0.00)

	def __unicode__(self):
		return "Cost - %s, %s" % (self.city.city, self.city.state)

	class Meta:
		verbose_name = 'Cost'
		verbose_name_plural = 'Costs'


TRENDLINE_TYPES = (
	('State', 'State'),
	('US', 'US'),
)

CHARTS = (
	('energy', 'Energy'),
	('water', 'Water'),
	('travel', 'Travel'),
	('waste', 'Waste'),
	('emissions', 'GHG Emissions'),
	('cost', 'Cost'),
)


class SpecialTrendLine(models.Model):
	type = models.CharField(max_length=100, choices=TRENDLINE_TYPES)
	chart = models.CharField(max_length=100, choices=CHARTS)
	year = models.CharField(max_length=4, help_text='ex: 2012')

	no_normalize = models.DecimalField(max_digits=16, decimal_places=4)
	capita_normalize = models.DecimalField(max_digits=16, decimal_places=4)
	household_normalize = models.DecimalField(max_digits=16, decimal_places=4)
	employment_normalize = models.DecimalField(max_digits=16, decimal_places=4)
	weather_normalize = models.DecimalField(max_digits=16, decimal_places=4)

	def __unicode__(self):
		return " %s -- %s" % (self.type, self.year)

	class Meta:
		verbose_name = 'Special Trend Line'
		verbose_name_plural = 'Special Trend Lines'
		ordering = ('year', 'type')