from django.db import models
from filebrowser.fields import FileBrowseField


HOME_PAGE_SECTIONS = (
    ('HOME', 'Home'),
    ('ENERGY', 'Energy'),
    ('WATER', 'Water'),
    ('TRAVEL', 'Travel'),
    ('WASTE', 'Waste'),
    ('CARBON', 'Carbon')
)


class HomePage_Section(models.Model):
    sect_type = models.CharField(max_length=20, choices=HOME_PAGE_SECTIONS)
    billboard_image = FileBrowseField(max_length=200, blank=True, null=True, help_text='1050px wide x 380px tall')
    graph_image = FileBrowseField(max_length=200, blank=True, null=True, help_text='1050px wide, 700px tall')
    graph_copy = models.TextField(max_length=2000, blank=True, null=True, help_text='')

    def __unicode__(self):
        return self.sect_type

    class Meta:
        verbose_name = 'Home Page Section'
        verbose_name_plural = 'Home Page Sections'


TEMPLATE_CHOICES = (
    ('home', 'Home Page Style'),
    ('energy', 'Energy Chart'),
    ('water', 'Water Chart'),
    ('travel', 'Travel Chart'),
    ('waste', 'Waste Chart'),
    ('emissions', 'Emissions Chart'),
    ('cost', 'Cost Chart'),
)


class WebPage(models.Model):
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    template_override = models.CharField(max_length=40, blank=True, null=True, choices=TEMPLATE_CHOICES)
    chart_title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(max_length=4000, blank=True, null=True, help_text='')

    def url(self):
        return '/%s' % self.slug

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Web Pages'
        verbose_name = 'Web Page'
        ordering = ('title',)


class HeaderLink(models.Model):
    title = models.CharField(max_length=50, help_text='This is the name of the link')

    direct_url = models.CharField(max_length=200, blank=True, null=True, help_text='Link directly to section on page.')
    web_page = models.ForeignKey(WebPage, blank=True, null=True)

    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def links(self):
        return self.headersublink_set.filter(is_active=True).order_by('display_order')

    def url(self):
        if (self.web_page != None) and (self.web_page.is_active == True):
            return self.web_page.url()

        return ''

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Header Links'
        verbose_name = 'Header Link'
        ordering = ('display_order', 'title')

    @staticmethod
    def GetActiveLinks():
        return HeaderLink.objects.filter(is_active=True)


class HeaderSubLink(models.Model):
    title = models.CharField(max_length=50)

    header_link = models.ForeignKey(HeaderLink)
    direct_url = models.CharField(max_length=200, blank=True, null=True)
    web_page = models.ForeignKey(WebPage, blank=True, null=True, help_text='Link directly to section on page.')

    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def url(self):
        if (self.web_page != None) and (self.web_page.is_active == True):
            return self.web_page.url()

        return '/'

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Header Sub Links'
        verbose_name = 'Header Sub Link'
        ordering = ('header_link', 'display_order', 'title')


class InPageLink(models.Model):
    title = models.CharField(max_length=50)
    title_detail = models.CharField(max_length=50, blank=True, null=True, help_text='Small text below the title.')

    bubble = FileBrowseField(max_length=200, help_text='185px wide by 195px tall')
    bubble_active = FileBrowseField(max_length=200, help_text='203px wide by 213px tall')

    teaser = models.CharField(max_length=150, blank=True, null=True, help_text='Black text for emphasis.')

    web_page = models.ForeignKey(WebPage, blank=True, null=True)

    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def url(self):
        if (self.web_page != None) and (self.web_page.is_active == True):
            return self.web_page.url()

        return '/'

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'In Page Links'
        verbose_name = 'In Page Link'
        ordering = ('title', 'display_order',)

    @staticmethod
    def GetActiveLinks():
        return InPageLink.objects.filter(is_active=True)