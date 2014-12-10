from site_content.models import HeaderLink

def setDetailContext(aContext):

	# Header Links
	headerLinks = HeaderLink.GetActiveLinks().order_by('display_order')
	aContext['headerLinks'] = headerLinks