from django.db import models
from django.urls import reverse
from django.utils.translation import get_language


def _pick(ar_val, en_val):
    lang = get_language() or 'ar'
    if lang.startswith('ar'):
        return ar_val or en_val or ''
    return en_val or ar_val or ''


class News(models.Model):
    title_ar = models.CharField('Title (AR)', max_length=250)
    title_en = models.CharField('Title (EN)', max_length=250)
    content_ar = models.TextField('Content (AR)')
    content_en = models.TextField('Content (EN)')
    image = models.ImageField('Image', upload_to='news/', blank=True, null=True)
    date = models.DateTimeField('Date', auto_now_add=True)
    is_published = models.BooleanField('Published', default=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-date']

    def __str__(self):
        return self.title_en or self.title_ar

    @property
    def title(self):
        return _pick(self.title_ar, self.title_en)

    @property
    def content(self):
        return _pick(self.content_ar, self.content_en)


class Announcement(models.Model):
    title_ar = models.CharField('Title (AR)', max_length=250)
    title_en = models.CharField('Title (EN)', max_length=250)
    date = models.DateTimeField('Date', auto_now_add=True)
    is_published = models.BooleanField('Published', default=True)

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-date']

    def __str__(self):
        return self.title_en or self.title_ar

    @property
    def title(self):
        return _pick(self.title_ar, self.title_en)


class GalleryImage(models.Model):
    title_ar = models.CharField('Title (AR)', max_length=200)
    title_en = models.CharField('Title (EN)', max_length=200)
    image = models.ImageField('Image', upload_to='gallery/')
    category = models.CharField('Category', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title_en or self.title_ar

    @property
    def title(self):
        return _pick(self.title_ar, self.title_en)


class Story(models.Model):
    member_name_ar = models.CharField('Member Name (AR)', max_length=200)
    member_name_en = models.CharField('Member Name (EN)', max_length=200)
    content_ar = models.TextField('Content (AR)')
    content_en = models.TextField('Content (EN)')
    image = models.ImageField('Image', upload_to='stories/', blank=True, null=True)
    date = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ['-date']

    def __str__(self):
        return self.member_name_en or self.member_name_ar

    @property
    def member_name(self):
        return _pick(self.member_name_ar, self.member_name_en)

    @property
    def content(self):
        return _pick(self.content_ar, self.content_en)


class TeamMember(models.Model):
    name_ar = models.CharField('Name (AR)', max_length=200)
    name_en = models.CharField('Name (EN)', max_length=200)
    role_ar = models.CharField('Role (AR)', max_length=200)
    role_en = models.CharField('Role (EN)', max_length=200)
    bio_ar = models.TextField('Bio (AR)', blank=True)
    bio_en = models.TextField('Bio (EN)', blank=True)
    image = models.ImageField('Image', upload_to='team/', blank=True, null=True)
    category = models.CharField('Category', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.name_en or self.name_ar

    @property
    def name(self):
        return _pick(self.name_ar, self.name_en)

    @property
    def role(self):
        return _pick(self.role_ar, self.role_en)

    @property
    def bio(self):
        return _pick(self.bio_ar, self.bio_en)


class HeroSlide(models.Model):
    title_ar    = models.CharField('Title (AR)', max_length=200)
    title_en    = models.CharField('Title (EN)', max_length=200)
    subtitle_ar = models.TextField('Subtitle (AR)', blank=True)
    subtitle_en = models.TextField('Subtitle (EN)', blank=True)
    image       = models.ImageField('Background Image', upload_to='hero/',
                                    help_text='Recommended: 1600 × 900 px or wider')
    cta1_text_ar = models.CharField('Button 1 Text (AR)', max_length=100, blank=True)
    cta1_text_en = models.CharField('Button 1 Text (EN)', max_length=100, blank=True)
    cta1_url     = models.CharField('Button 1 URL', max_length=200, blank=True,
                                    help_text='Full path e.g. /ar/contact/ — leave blank for Contact page')
    cta2_text_ar = models.CharField('Button 2 Text (AR)', max_length=100, blank=True)
    cta2_text_en = models.CharField('Button 2 Text (EN)', max_length=100, blank=True)
    cta2_url     = models.CharField('Button 2 URL', max_length=200, blank=True,
                                    help_text='Full path e.g. /ar/team/ — leave blank for Team page')
    order     = models.PositiveIntegerField('Order', default=0, help_text='Lower = appears first')
    is_active = models.BooleanField('Active', default=True)

    class Meta:
        verbose_name        = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'
        ordering            = ['order']

    def __str__(self):
        return self.title_en or self.title_ar

    @property
    def title(self):    return _pick(self.title_ar,    self.title_en)
    @property
    def subtitle(self): return _pick(self.subtitle_ar, self.subtitle_en)
    @property
    def cta1_text(self): return _pick(self.cta1_text_ar, self.cta1_text_en)
    @property
    def cta2_text(self): return _pick(self.cta2_text_ar, self.cta2_text_en)

    def get_cta1_url(self):
        if self.cta1_url:
            return self.cta1_url
        return reverse('main:contact')

    def get_cta2_url(self):
        if self.cta2_url:
            return self.cta2_url
        return reverse('main:team')


class SiteSetting(models.Model):
    stat1_number   = models.CharField('Stat 1 — Number',      max_length=20,  default='1,000+')
    stat1_label_ar = models.CharField('Stat 1 — Label (AR)',  max_length=100, default='طالب ملتحق')
    stat1_label_en = models.CharField('Stat 1 — Label (EN)',  max_length=100, default='Students Enrolled')

    stat2_number   = models.CharField('Stat 2 — Number',      max_length=20,  default='15+')
    stat2_label_ar = models.CharField('Stat 2 — Label (AR)',  max_length=100, default='لغة مُدرَّسة')
    stat2_label_en = models.CharField('Stat 2 — Label (EN)',  max_length=100, default='Languages Taught')

    stat3_number   = models.CharField('Stat 3 — Number',      max_length=20,  default='20+')
    stat3_label_ar = models.CharField('Stat 3 — Label (AR)',  max_length=100, default='برنامج متاح')
    stat3_label_en = models.CharField('Stat 3 — Label (EN)',  max_length=100, default='Programs Offered')

    stat4_number   = models.CharField('Stat 4 — Number',      max_length=20,  default='400+')
    stat4_label_ar = models.CharField('Stat 4 — Label (AR)',  max_length=100, default='خريج')
    stat4_label_en = models.CharField('Stat 4 — Label (EN)',  max_length=100, default='Alumni')

    # ── Footer ────────────────────────────────────────────────────────────
    footer_desc_ar = models.TextField(
        'Footer Description (AR)', blank=True,
        default='تعزيز تعلّم اللغات وتبادل الثقافات في جامعة النجاح الوطنية، نابلس، فلسطين.')
    footer_desc_en = models.TextField(
        'Footer Description (EN)', blank=True,
        default='Promoting language learning and cultural exchange at An-Najah National University, Nablus, Palestine.')

    # ── Social media ──────────────────────────────────────────────────────
    facebook_url  = models.URLField('Facebook URL',  blank=True,
                                    help_text='Leave blank to hide the icon')
    instagram_url = models.URLField('Instagram URL', blank=True,
                                    help_text='Leave blank to hide the icon')
    youtube_url   = models.URLField('YouTube URL',   blank=True,
                                    help_text='Leave blank to hide the icon')
    linkedin_url  = models.URLField('LinkedIn URL',  blank=True,
                                    help_text='Leave blank to hide the icon')

    # ── Contact ───────────────────────────────────────────────────────────
    contact_address_ar = models.CharField('Address (AR)', max_length=300, blank=True,
                                          default='نابلس، الضفة الغربية، فلسطين')
    contact_address_en = models.CharField('Address (EN)', max_length=300, blank=True,
                                          default='Nablus, West Bank, Palestine')
    contact_email = models.EmailField('Email', blank=True, default='lrc@najah.edu')
    contact_phone = models.CharField('Phone', max_length=50, blank=True, default='+970 9 234 5113')

    class Meta:
        verbose_name        = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def stat1_label(self): return _pick(self.stat1_label_ar, self.stat1_label_en)
    @property
    def stat2_label(self): return _pick(self.stat2_label_ar, self.stat2_label_en)
    @property
    def stat3_label(self): return _pick(self.stat3_label_ar, self.stat3_label_en)
    @property
    def stat4_label(self): return _pick(self.stat4_label_ar, self.stat4_label_en)
    @property
    def footer_desc(self): return _pick(self.footer_desc_ar, self.footer_desc_en)
    @property
    def contact_address(self): return _pick(self.contact_address_ar, self.contact_address_en)


class Page(models.Model):
    title_ar = models.CharField('Title (AR)', max_length=200)
    title_en = models.CharField('Title (EN)', max_length=200)
    content_ar = models.TextField('Content (AR)')
    content_en = models.TextField('Content (EN)')
    banner_image = models.ImageField('Banner Image', upload_to='pages/', blank=True, null=True,
                                     help_text='Full-width hero image. Recommended: 1400 × 600 px')
    slug = models.SlugField('URL Slug', unique=True, max_length=100,
                            help_text='Short URL identifier, e.g. "about-us"')
    show_in_nav = models.BooleanField('Show in Navbar', default=True)
    nav_order = models.PositiveIntegerField('Navbar Order', default=0,
                                            help_text='Lower number = appears first')
    is_published = models.BooleanField('Published', default=True)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['nav_order', 'title_en']

    def __str__(self):
        return self.title_en or self.title_ar

    def get_absolute_url(self):
        return reverse('main:page', kwargs={'slug': self.slug})

    @property
    def title(self):
        return _pick(self.title_ar, self.title_en)

    @property
    def content(self):
        return _pick(self.content_ar, self.content_en)
