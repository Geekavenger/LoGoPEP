import logging
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from site_content.models import WebPage, InPageLink, HomePage_Section
from utility import setDetailContext
from city_metrics.views import viewEnergyChart, viewWaterChart, viewWasteChart, viewTravelChart, viewEmissionsChart, viewCostChart


def viewHomeStyle(request, page):
    current_section = HomePage_Section.objects.get('sect_type' == 'ENERGY')

    context = {'page': page, 'current_sect': current_section}
    setDetailContext(context)

    return render_to_response('home.html', context)


# Some templates need extra or special processing to retrieve additional data. This map
# defines which templates get a special controller.

TEMPLATE_CONTROLLER_MAP = {'home': viewHomeStyle, 'energy': viewEnergyChart, 'water': viewWaterChart, 'waste': viewWasteChart,
                           'travel': viewTravelChart, 'emissions': viewEmissionsChart, 'cost': viewCostChart}


def viewDetail(request, aSlug):
    try:
        page = WebPage.objects.get(slug=aSlug, is_active=True)

    except Exception, e:
        logging.error(e)
        return HttpResponseNotFound()

    if page.template_override != None and len(page.template_override) > 1:

        if TEMPLATE_CONTROLLER_MAP.has_key(page.template_override):
            func_ptr = TEMPLATE_CONTROLLER_MAP[page.template_override]
            return func_ptr(request, page)

    context = {'page': page, }
    setDetailContext(context)

    return render_to_response('detail_page.html', context)