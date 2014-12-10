from django.conf.urls import patterns

urlpatterns = patterns('admin_imports.views',
	(r'^demographic-data-importer/$', 'demographicDataImporter'),
	(r'^energy-importer/$', 'energyImporter'),
	(r'^water-importer/$', 'waterImporter'),
	(r'^travel-importer/$', 'travelImporter'),
	(r'^waste-importer/$', 'wasteImporter'),
	(r'^emissions-importer/$', 'emissionsImporter'),
	(r'^cost-importer/$', 'costImporter'),
)