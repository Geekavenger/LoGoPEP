import json
import logging
from django.http import HttpResponse
from django.shortcuts import render_to_response
from site_content.models import WebPage, InPageLink, HomePage_Section
from utility import setDetailContext


def viewHome(request):
    try:
        page = WebPage.objects.get(is_active=True, slug='home')
        current_section = HomePage_Section.objects.get(sect_type='HOME')

    except Exception, e:
        logging.error(e)
        current_section = None
        page = None

    context = {'page': page, 'current_sect': current_section}
    setDetailContext(context)

    return render_to_response('home.html', context)


def selectHomePageSect(request):
    json_data = {}

    if request.GET['sect']:
        sect_id = request.GET['sect']
        section = HomePage_Section.objects.get(sect_type=sect_id)
        json_data['billboardUrl'] = str(section.billboard_image)
        json_data['graphUrl'] = str(section.graph_image)
        json_data['textHtml'] = str(section.graph_copy)
        json_data['sect'] = sect_id

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def viewParticipationForm(request):
    context = {}
    setDetailContext(context)

    return render_to_response('forms/participation_form.html', context)
