from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import gdata.analytics.client
import datetime
from webapp import settings

analytics_email = settings.ANALYTICS_EMAIL
analytics_password = settings.ANALYTICS_PASSWORD
table_id = settings.ANALYTICS_TABLE_ID


@login_required()
def view_analytics(request):
    title = 'Analytics'

    if request.method == 'POST':
        data = request.POST.copy()

        from_date = data['FromDate']
        thru_date = data['ThruDate']

        from_date_parsed = datetime.datetime.strptime(from_date, "%m/%d/%Y")
        thru_date_parsed = datetime.datetime.strptime(thru_date, "%m/%d/%Y")
    else:
        from_date_parsed = datetime.date.today() + datetime.timedelta(days=-30)
        thru_date_parsed = datetime.date.today()

    from_date_str = from_date_parsed.strftime("%m/%d/%Y")
    thru_date_str = thru_date_parsed.strftime("%m/%d/%Y")
    from_date_google = from_date_parsed.strftime("%Y-%m-%d")
    thru_date_google = thru_date_parsed.strftime("%Y-%m-%d")

    source_app_name = 'analytics'
    my_client = gdata.analytics.client.AnalyticsClient(source=source_app_name)
    try:
        my_client.client_login(analytics_email, analytics_password, source=source_app_name,
                               service='analytics')
    except gdata.client.BadAuthentication:
        print 'Invalid user credentials given.'
    except gdata.client.Error:
        print 'Login Error'

    # DataFeedQuery simplifies constructing API queries and uri encodes params.

    ##### All Visitors #####
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': from_date_google,
        'end-date': thru_date_google,
        'dimensions': 'ga:date',
        'metrics': 'ga:visits,ga:newVisits',
        'sort': 'ga:date',
        'output': 'dataTable'
    })
    visitor_feed = my_client.GetDataFeed(data_query)

    ##### Page View Query #####
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': from_date_google,
        'end-date': thru_date_google,
        'dimensions': 'ga:date',
        'metrics': 'ga:pageViews,ga:uniquePageViews',
        'sort': 'ga:date',
        'output': 'dataTable'
    })
    page_view_feed = my_client.GetDataFeed(data_query)

    ##### Bounce Rate Query #####
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': from_date_google,
        'end-date': thru_date_google,
        'dimensions': 'ga:date',
        'metrics': 'ga:exitRate',
        'sort': 'ga:date',
        'output': 'dataTable'
    })
    bounce_rate_feed = my_client.GetDataFeed(data_query)

    ##### Referral Query #####
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': from_date_google,
        'end-date': thru_date_google,
        'dimensions': 'ga:source',
        'metrics': 'ga:visits,ga:newVisits,ga:bounces',
        'sort': '-ga:visits,ga:source',
        'filters': 'ga:medium==organic',
        'max-results': '10'
    })
    referral_feed = my_client.GetDataFeed(data_query)

    ##### Browser Query #####
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': from_date_google,
        'end-date': thru_date_google,
        'dimensions': 'ga:browser',
        'metrics': 'ga:visits,ga:newVisits,ga:bounces',
        'sort': '-ga:visits',
        'filters': 'ga:medium==organic',
        'max-results': '10'
    })
    browser_feed = my_client.GetDataFeed(data_query)

    ##### Operating System Query #####
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': from_date_google,
        'end-date': thru_date_google,
        'dimensions': 'ga:operatingSystem',
        'metrics': 'ga:visits,ga:newVisits,ga:bounces',
        'sort': '-ga:visits',
        'filters': 'ga:medium==organic',
        'max-results': '10'
    })
    os_feed = my_client.GetDataFeed(data_query)

    ##### Search Term Query #####
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': from_date_google,
        'end-date': thru_date_google,
        'dimensions': 'ga:keyword',
        'metrics': 'ga:visits,ga:newVisits,ga:bounces',
        'sort': '-ga:visits',
        'filters': 'ga:medium==organic',
        'max-results': '10'
    })
    search_feed = my_client.GetDataFeed(data_query)

    context = {'title': title, 'fromdate': from_date_str, 'thrudate': thru_date_str, 'visitorFeed': visitor_feed,
               'pageViewFeed': page_view_feed, 'bounceRateFeed': bounce_rate_feed, 'referralFeed': referral_feed,
               'browserFeed': browser_feed,
               'osFeed': os_feed, 'searchFeed': search_feed}

    template = 'admin/analytics.html'

    return render_to_response(template, context, context_instance=RequestContext(request))

