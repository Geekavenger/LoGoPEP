from django.contrib import admin
from models import *


class CityAdmin(admin.ModelAdmin):
	list_display = ('city', 'state', 'type', 'sort_order',)
	list_filter = ('city', 'state', 'type', 'sort_order',)


class DemographicDataAdmin(admin.ModelAdmin):
	list_display = ('city', 'population', 'jobs', 'households', 'year',)
	list_filter = ('city', 'year',)


class EnergyAdmin(admin.ModelAdmin):
	list_display = ('city', 'year',)
	list_filter = ('city', 'year',)

	fieldsets = (
		('General Info', {
			'fields': ('city', 'year')
		}),
		('By Type', {
			'fields': ('electricity', 'natural_gas', 'other')
		}),
		('WN By Type (WN = Weather Normalized)', {
			'fields': ('wn_electricity', 'wn_natural_gas', 'wn_other')
		}),
		('Totals By Use', {
			'fields': ('total_res_energy', 'total_com_ind_energy',)
		}),
		('WN Totals By Use', {
			'fields': ('wn_total_res_energy', 'wn_total_com_ind_energy',)
		}),
	)


class WaterAdmin(admin.ModelAdmin):
	list_display = ('city', 'year',)
	list_filter = ('city', 'year',)

	fieldsets = (
		('General Info', {
			'fields': ('city', 'year')
		}),
		('Totals By Use', {
			'fields': ('total_res_water', 'total_com_ind_water',)
		}),
	)


class TravelAdmin(admin.ModelAdmin):
	list_display = ('city', 'year',)
	list_filter = ('city', 'year',)

	fieldsets = (
		('General Info', {
			'fields': ('city', 'year')
		}),
		('Totals By Use', {
			'fields': ('total_vmt',)
		}),
	)


class WasteAdmin(admin.ModelAdmin):
	list_display = ('city', 'year',)
	list_filter = ('city', 'year',)

	fieldsets = (
		('General Info', {
			'fields': ('city', 'year')
		}),
		('Totals By Use', {
			'fields': ('recycled', 'landfilled', 'incinerated')
		}),
	)


class EmissionsAdmin(admin.ModelAdmin):
	list_display = ('city', 'year',)
	list_filter = ('city', 'year',)

	fieldsets = (
		('General Info', {
			'fields': ('city', 'year')
		}),
		('Totals', {
			'fields': ('energy_associated_emissions', 'water_associated_emissions', 'travel_associated_emissions', 'waste_associated_emissions')
		}),
		('WN Totals', {
			'fields': ('wn_energy_associated_emissions', 'wn_water_associated_emissions', 'wn_travel_associated_emissions', 'wn_waste_associated_emissions')
		}),
		('Energy Numbers', {
			'fields': ('energy_type_electricity', 'energy_type_natural_gas', 'energy_type_other', 'energy_use_residential', 'energy_use_com_ind',
			'wn_energy_type_electricity', 'wn_energy_type_natural_gas', 'wn_energy_type_other', 'wn_energy_use_residential', 'wn_energy_use_com_ind')
		}),
		('Waste Numbers', {
			'fields': ('waste_method_recycled', 'waste_method_landfilled', 'waste_method_incinerated')
		})
	)


class CostAdmin(admin.ModelAdmin):
	list_display = ('city', 'year',)
	list_filter = ('city', 'year',)

	fieldsets = (
		('General Info', {
			'fields': ('city', 'year')
		}),
		('Totals By Source', {
			'fields': ('water_associated_costs', 'travel_associated_costs', 'waste_associated_costs')
		}),
		('Energy Numbers', {
			'fields': ('energy_associated_costs', 'energy_type_electricity', 'energy_type_natural_gas', 'energy_type_other',
			'energy_use_residential', 'energy_use_com_ind')
		}),
		('WN Energy Numbers', {
			'fields': ('wn_energy_associated_costs', 'wn_energy_type_electricity', 'wn_energy_type_natural_gas', 'wn_energy_type_other',
			'wn_energy_use_residential', 'wn_energy_use_com_ind')
		}),
		('Water Numbers', {
			'fields': ('water_use_residential', 'water_use_com_ind')
		}),
		('Waste Numbers', {
			'fields': ('waste_method_recycled', 'waste_method_landfilled', 'waste_method_incinerated')
		})
	)


class SpecialTrendLineAdmin(admin.ModelAdmin):
	list_display = ('type', 'year',)
	list_filter = ('type', 'year',)


admin.site.register(City, CityAdmin)
admin.site.register(DemographicData, DemographicDataAdmin)
admin.site.register(Energy, EnergyAdmin)
admin.site.register(Water, WaterAdmin)
admin.site.register(Travel, TravelAdmin)
admin.site.register(Waste, WasteAdmin)
admin.site.register(Emissions, EmissionsAdmin)
admin.site.register(Cost, CostAdmin)
admin.site.register(SpecialTrendLine, SpecialTrendLineAdmin)