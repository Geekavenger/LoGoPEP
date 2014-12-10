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

    if request.POST:
        sect_id = request.POST['sect']
        section = HomePage_Section.objects.get(sect_type=sect_id)
        json_data['billboardUrl'] = section.billboard_image.url
        json_data['graphUrl'] = section.graph_image.url
        json_data['textHtml'] = section.graph_copy
        json_data['sect'] = sect_id

        return HttpResponse(json.dumps(json_data), mimetype='application/json')


def viewParticipationForm(request):
    context = {}
    setDetailContext(context)

    return render_to_response('forms/participation_form.html', context)