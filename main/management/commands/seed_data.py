import os
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand

from main.models import Announcement, GalleryImage, HeroSlide, News, Page, SiteSetting, Story, TeamMember

PICSUM = 'https://picsum.photos/seed'


def _img(seed, folder, w=800, h=450):
    """Download from picsum.photos into media/<folder>/<seed>.jpg.
    Returns the relative path suitable for an ImageField, or '' on failure."""
    dest_dir = os.path.join(settings.MEDIA_ROOT, folder)
    os.makedirs(dest_dir, exist_ok=True)
    filename = f'{seed}.jpg'
    filepath = os.path.join(dest_dir, filename)
    if not os.path.exists(filepath):
        try:
            url = f'{PICSUM}/{seed}/{w}/{h}'
            urllib.request.urlretrieve(url, filepath)
        except Exception:
            return ''
    return f'{folder}/{filename}'


class Command(BaseCommand):
    help = 'Populate the database with sample Arabic/English content and placeholder images'

    def handle(self, *args, **options):
        self._clear()
        self._hero_slides()
        self._site_settings()
        self._news()
        self._announcements()
        self._stories()
        self._team()
        self._gallery()
        self._pages()
        self.stdout.write(self.style.SUCCESS('Sample data created.'))

    def _clear(self):
        HeroSlide.objects.all().delete()
        SiteSetting.objects.all().delete()
        News.objects.all().delete()
        Announcement.objects.all().delete()
        Story.objects.all().delete()
        TeamMember.objects.all().delete()
        GalleryImage.objects.all().delete()
        Page.objects.all().delete()
        self.stdout.write('  Cleared existing data.')

    def _hero_slides(self):
        slides = [
            {
                'title_ar':    'فتح آفاق التواصل العالمي',
                'title_en':    'Unlocking Global Communication',
                'subtitle_ar': 'نُمكِّن الطلبة من الالتحاق ببرامج لغوية متميزة تجسر الثقافات وتبني المهارات وتفتح أبواب الفرص العالمية.',
                'subtitle_en': 'Empowering students in high-quality language programs that connect cultures, build skills, and open doors to global opportunities.',
                'cta1_text_ar': 'استكشف البرامج',
                'cta1_text_en': 'Explore Programs',
                'cta2_text_ar': 'تعرّف على فريقنا',
                'cta2_text_en': 'Meet Our Team',
                'seed': 'lrc_hero_1', 'order': 1,
            },
            {
                'title_ar':    'بيئة تعليمية احترافية',
                'title_en':    'A Professional Learning Environment',
                'subtitle_ar': 'مركز متخصص يوفر أحدث الأساليب التعليمية في تعلّم اللغات الإنجليزية والفرنسية والألمانية والإسبانية.',
                'subtitle_en': 'A specialized center offering the latest methodologies in English, French, German, and Spanish language education.',
                'cta1_text_ar': 'تواصل معنا',
                'cta1_text_en': 'Contact Us',
                'cta2_text_ar': 'قصص النجاح',
                'cta2_text_en': 'Success Stories',
                'seed': 'lrc_hero_2', 'order': 2,
            },
            {
                'title_ar':    'جسر بين الثقافات والحضارات',
                'title_en':    'Bridging Cultures and Civilizations',
                'subtitle_ar': 'نؤمن بأن اللغة هي المفتاح لفهم الثقافات الأخرى وبناء علاقات إنسانية راسخة.',
                'subtitle_en': 'We believe that language is the key to understanding other cultures and building lasting human connections.',
                'cta1_text_ar': 'أخبارنا',
                'cta1_text_en': 'Our News',
                'cta2_text_ar': 'معرض الصور',
                'cta2_text_en': 'Photo Gallery',
                'seed': 'lrc_hero_3', 'order': 3,
            },
        ]
        for d in slides:
            seed = d.pop('seed')
            img = _img(seed, 'hero', 1600, 900)
            if img:
                HeroSlide.objects.create(image=img, **d)
        self.stdout.write(f'  Created {HeroSlide.objects.count()} hero slides.')

    def _site_settings(self):
        SiteSetting.objects.get_or_create(pk=1)
        self.stdout.write('  Site settings initialized.')

    def _news(self):
        items = [
            {
                'title_ar': 'مسابقة اللغة الإنجليزية السنوية تنطلق في جامعة النجاح',
                'title_en': 'Annual English Language Competition Kicks Off at An-Najah University',
                'content_ar': (
                    'أعلن مركز الموارد اللغوية في جامعة النجاح الوطنية عن انطلاق مسابقة اللغة الإنجليزية '
                    'السنوية للعام الأكاديمي الحالي، وذلك بمشاركة أكثر من مئة وخمسين طالباً وطالبة من '
                    'مختلف الكليات. تهدف المسابقة إلى تعزيز المهارات اللغوية لدى الطلبة وتشجيعهم على '
                    'التواصل باللغة الإنجليزية في المحافل الأكاديمية والمهنية.'
                ),
                'content_en': (
                    'The Language Resource Center at An-Najah National University has announced the launch '
                    'of its annual English Language Competition for the current academic year, with the '
                    'participation of over one hundred and fifty students from various faculties. The '
                    'competition aims to enhance students\' linguistic skills and encourage communication '
                    'in academic and professional settings.'
                ),
                'seed': 'lrc_news_1',
            },
            {
                'title_ar': 'أسبوع الثقافة الفرنسية يُطلق فعالياته في رحاب الجامعة',
                'title_en': 'French Culture Week Launches Its Activities on Campus',
                'content_ar': (
                    'احتضنت جامعة النجاح الوطنية فعاليات أسبوع الثقافة الفرنسية الذي نظّمه مركز الموارد '
                    'اللغوية بالتعاون مع المعهد الثقافي الفرنسي في فلسطين. تضمّنت الفعاليات عروضاً سينمائية '
                    'وأمسيات شعرية ومعارض للفن التشكيلي الفرنسي، فضلاً عن ورشات عمل تعريفية باللغة الفرنسية.'
                ),
                'content_en': (
                    'An-Najah National University hosted French Culture Week, organized by the Language '
                    'Resource Center in cooperation with the French Cultural Institute in Palestine. '
                    'The event included film screenings, poetry evenings, and French fine art exhibitions, '
                    'as well as introductory workshops on the French language and culture.'
                ),
                'seed': 'lrc_news_2',
            },
            {
                'title_ar': 'مركز الموارد اللغوية يُطلق دورات جديدة في الألمانية والإسبانية',
                'title_en': 'LRC Launches New German and Spanish Language Courses',
                'content_ar': (
                    'أعلن مركز الموارد اللغوية عن إطلاق دورات تدريبية جديدة في اللغتين الألمانية والإسبانية، '
                    'استجابةً للطلب المتزايد من قِبل الطلبة وأبناء المجتمع المحلي. تُقدَّم الدورات على '
                    'ثلاثة مستويات: مبتدئ ومتوسط ومتقدم.'
                ),
                'content_en': (
                    'The Language Resource Center has announced new training courses in German and Spanish, '
                    'in response to increasing demand from students and community members. The courses are '
                    'offered at three levels: beginner, intermediate, and advanced.'
                ),
                'seed': 'lrc_news_3',
            },
            {
                'title_ar': 'برنامج التبادل الثقافي يُوسّع آفاق طلبة جامعة النجاح',
                'title_en': 'Cultural Exchange Program Broadens Horizons for An-Najah Students',
                'content_ar': (
                    'أتاح برنامج التبادل الثقافي لعشرين طالباً وطالبة فرصة التواصل المباشر مع نظرائهم من '
                    'جامعات أوروبية وأمريكية. يمتد البرنامج على مدار الفصل الدراسي ويشتمل على جلسات نقاش '
                    'أسبوعية ومشاريع مشتركة وزيارات ميدانية متبادلة.'
                ),
                'content_en': (
                    'The cultural exchange program has given twenty students the opportunity to connect '
                    'with counterparts from European and American universities. The program spans an '
                    'entire semester and includes weekly discussion sessions, joint projects, and '
                    'reciprocal field visits.'
                ),
                'seed': 'lrc_news_4',
            },
            {
                'title_ar': 'ورشة الترجمة الأدبية تستقطب نخبة من المثقفين والأكاديميين',
                'title_en': 'Literary Translation Workshop Attracts Academics and Intellectuals',
                'content_ar': (
                    'نظّم مركز الموارد اللغوية ورشة عمل متخصصة في الترجمة الأدبية استقطبت نخبة من '
                    'الأكاديميين والمترجمين والكتّاب من مختلف أنحاء فلسطين. ركّزت الورشة على تقنيات '
                    'ترجمة النصوص الشعرية والسردية بين العربية والإنجليزية.'
                ),
                'content_en': (
                    'The LRC organized a specialized literary translation workshop attracting academics, '
                    'translators, and writers from across Palestine. The workshop focused on techniques '
                    'for translating poetic and narrative texts between Arabic and English.'
                ),
                'seed': 'lrc_news_5',
            },
            {
                'title_ar': 'طلبة المركز يحصدون جوائز في مسابقة الخطاب على مستوى المحافظة',
                'title_en': 'LRC Students Win Awards at Governorate-Level Speech Competition',
                'content_ar': (
                    'حقّق طلبة مركز الموارد اللغوية نتائج مشرّفة في مسابقة خطاب المدن. فاز الطلبة بثلاث '
                    'جوائز في فئات الخطابة العربية والإنجليزية والمناظرة.'
                ),
                'content_en': (
                    'LRC students achieved outstanding results at the governorate-level speech competition. '
                    'They won three awards in Arabic oratory, English oratory, and debate categories.'
                ),
                'seed': 'lrc_news_6',
            },
        ]
        for d in items:
            seed = d.pop('seed')
            img = _img(seed, 'news')
            obj = News(**d)
            if img:
                obj.image = img
            obj.save()
        self.stdout.write(f'  Created {len(items)} news items.')

    def _announcements(self):
        items = [
            {'title_ar': 'التسجيل في دورات الفصل الصيفي مفتوح حتى نهاية الشهر',
             'title_en': 'Summer Session Course Registration Open Until End of Month'},
            {'title_ar': 'اجتماع طلبة المستوى المتقدم — قاعة المركز الرئيسية',
             'title_en': 'Advanced Level Students Meeting — Main Hall'},
            {'title_ar': 'عطلة رسمية: سيكون المركز مغلقاً الخميس والجمعة القادمَين',
             'title_en': 'Official Holiday: Center Closed This Thursday and Friday'},
            {'title_ar': 'نتائج مسابقة اللغة الإنجليزية ستُعلَن خلال 48 ساعة',
             'title_en': 'English Competition Results Will Be Announced Within 48 Hours'},
            {'title_ar': 'متاح الآن: مكتبة الصوتيات والمرئيات في الطابق الثاني',
             'title_en': 'Now Available: Audio-Visual Library on the Second Floor'},
            {'title_ar': 'آخر موعد لتسليم مشاريع الترجمة هو الأحد القادم',
             'title_en': 'Translation Projects Deadline Is Next Sunday'},
        ]
        for d in items:
            Announcement.objects.create(**d)
        self.stdout.write(f'  Created {len(items)} announcements.')

    def _stories(self):
        items = [
            {
                'member_name_ar': 'رنا الحمدان',
                'member_name_en': 'Rana Al-Hamdan',
                'content_ar': 'التحقتُ بمركز الموارد اللغوية وأنا أكاد لا أستطيع صياغة جملة إنجليزية كاملة. بعد عام واحد من التدريب المكثّف نجحتُ في اجتياز اختبار الآيلتس بدرجة 7.5، وقُبلتُ في برنامج ماجستير في جامعة بريطانية مرموقة.',
                'content_en': 'I joined the LRC barely able to form a complete English sentence. After one year of intensive training I passed the IELTS with a 7.5 and was accepted into a Master\'s program at a prestigious British university.',
                'seed': 'lrc_story_1',
            },
            {
                'member_name_ar': 'كريم أبو عيشة',
                'member_name_en': 'Karim Abu Aisha',
                'content_ar': 'كانت اللغة الفرنسية مجرد حلم بعيد المنال قبل أن أنضم إلى المركز. اليوم، بعد ثلاث سنوات من الدراسة، أعمل مترجماً فورياً في مؤتمرات دولية.',
                'content_en': 'French was just a distant dream before joining the Center. Today, after three years of study, I work as a simultaneous interpreter at international conferences.',
                'seed': 'lrc_story_2',
            },
            {
                'member_name_ar': 'سارة عوض',
                'member_name_en': 'Sara Awad',
                'content_ar': 'لم أتخيّل يوماً أن أجد نفسي أُلقي خطاباً أمام جمهور دولي. المركز منحني الأدوات اللغوية والثقة بالنفس اللازمتَين لذلك. فزتُ بالمرتبة الأولى في مسابقة الخطابة الإنجليزية على المستوى الوطني.',
                'content_en': 'I never imagined I would find myself delivering a speech before an international audience. The Center gave me the tools and confidence to do so. I won first place in the national English oratory competition.',
                'seed': 'lrc_story_3',
            },
            {
                'member_name_ar': 'يوسف الخطيب',
                'member_name_en': 'Yusuf Al-Khatib',
                'content_ar': 'كنت أعاني من الخجل الشديد عند التحدث بالإنجليزية، لكن المناخ الدافئ الذي يوفّره المركز ساعدني على تجاوز هذا الحاجز. اليوم أعمل في شركة تقنية دولية.',
                'content_en': 'I used to suffer from severe shyness when speaking English, but the warm environment of the Center helped me overcome this. Today I work at an international tech company.',
                'seed': 'lrc_story_4',
            },
            {
                'member_name_ar': 'لمى نصر',
                'member_name_en': 'Lama Nasr',
                'content_ar': 'أفادتني دورات الكتابة الأكاديمية في المركز فائدة كبيرة إبّان إعداد رسالة الدكتوراه. نُشر جزء من أطروحتي في مجلة دولية محكّمة.',
                'content_en': 'The academic writing courses proved invaluable during my doctoral thesis. Part of my thesis was published in a peer-reviewed international journal.',
                'seed': 'lrc_story_5',
            },
            {
                'member_name_ar': 'عمر شاهين',
                'member_name_en': 'Omar Shaheen',
                'content_ar': 'بدأتُ رحلتي مع الألمانية من الصفر في المركز. بعد عامين أصبحتُ أحمل شهادة B2 وقُبلتُ في برنامج منحة دراسية ممولّة بالكامل في ألمانيا.',
                'content_en': 'I started German from scratch at the Center. After two years I held a B2 certificate and was accepted into a fully funded scholarship in Germany.',
                'seed': 'lrc_story_6',
            },
        ]
        for d in items:
            seed = d.pop('seed')
            img = _img(seed, 'stories', 300, 300)
            obj = Story(**d)
            if img:
                obj.image = img
            obj.save()
        self.stdout.write(f'  Created {len(items)} stories.')

    def _team(self):
        items = [
            {
                'name_ar': 'د. محمد العمري',
                'name_en': 'Dr. Mohammad Al-Omari',
                'role_ar': 'مدير المركز',
                'role_en': 'Center Director',
                'bio_ar': 'دكتوراه في اللغويات التطبيقية من جامعة إكستر. خمسة عشر عاماً في تعليم اللغات وإدارة المراكز اللغوية.',
                'bio_en': 'PhD in Applied Linguistics from the University of Exeter. Fifteen years in language teaching and center management.',
                'category': 'leadership', 'seed': 'lrc_team_1',
            },
            {
                'name_ar': 'أ. سوزان ريان',
                'name_en': 'Ms. Susan Ryan',
                'role_ar': 'منسّقة اللغة الإنجليزية',
                'role_en': 'English Language Coordinator',
                'bio_ar': 'ماجستير في تعليم الإنجليزية للناطقين بغيرها. متخصصة في تصميم المناهج والكتابة الأكاديمية.',
                'bio_en': 'MA in TESOL. Specializes in curriculum design and academic writing.',
                'category': 'academic', 'seed': 'lrc_team_2',
            },
            {
                'name_ar': 'أ. نادر سلامة',
                'name_en': 'Mr. Nader Salama',
                'role_ar': 'منسّق اللغة الفرنسية',
                'role_en': 'French Language Coordinator',
                'bio_ar': 'متخرج من معهد الدراسات السياسية في باريس. يُدير البرامج الثقافية الفرنسية.',
                'bio_en': 'Graduate of Sciences Po Paris. Manages French cultural programs.',
                'category': 'academic', 'seed': 'lrc_team_3',
            },
            {
                'name_ar': 'أ. هالة أبو غوش',
                'name_en': 'Ms. Hala Abu Ghosh',
                'role_ar': 'مسؤولة الفعاليات والشراكات',
                'role_en': 'Events & Partnerships Officer',
                'bio_ar': 'خبرة تزيد على عشر سنوات في إدارة الفعاليات الثقافية وبناء شراكات مع المؤسسات الدولية.',
                'bio_en': 'Over ten years managing cultural events and international institutional partnerships.',
                'category': 'admin', 'seed': 'lrc_team_4',
            },
            {
                'name_ar': 'أ. طارق حمدان',
                'name_en': 'Mr. Tariq Hamdan',
                'role_ar': 'منسّق الألمانية والإسبانية',
                'role_en': 'German & Spanish Coordinator',
                'bio_ar': 'شهادة DAAD في الألمانية ودرجة DELE المتقدمة في الإسبانية.',
                'bio_en': 'DAAD certificate in German and advanced DELE in Spanish.',
                'category': 'academic', 'seed': 'lrc_team_5',
            },
            {
                'name_ar': 'أ. منى الجعبري',
                'name_en': 'Ms. Mona Al-Jabari',
                'role_ar': 'مسؤولة الإرشاد الطلابي',
                'role_en': 'Student Guidance Officer',
                'bio_ar': 'متخصصة في الإرشاد الأكاديمي ودعم الطلبة المتقدمين للدراسة في الخارج.',
                'bio_en': 'Specializes in academic counseling and supporting students applying to study abroad.',
                'category': 'admin', 'seed': 'lrc_team_6',
            },
            {
                'name_ar': 'م. أحمد صبري',
                'name_en': 'Eng. Ahmad Sabri',
                'role_ar': 'مسؤول التقنية والمحتوى الرقمي',
                'role_en': 'Technology & Digital Content',
                'bio_ar': 'مطوّر ويب وخبير في التعليم الإلكتروني. يُشرف على المنصة الرقمية للمركز.',
                'bio_en': 'Web developer and e-learning expert. Oversees the Center\'s digital platform.',
                'category': 'admin', 'seed': 'lrc_team_7',
            },
            {
                'name_ar': 'أ. ديمة نور',
                'name_en': 'Ms. Dima Nour',
                'role_ar': 'مدرّبة مهارات التواصل',
                'role_en': 'Communication Skills Trainer',
                'bio_ar': 'متخصصة في تدريب مهارات الخطابة والتفاوض والعرض. تدرّبت في مؤسسات دولية في أوروبا.',
                'bio_en': 'Specialist in oratory, negotiation, and presentation skills training.',
                'category': 'academic', 'seed': 'lrc_team_8',
            },
        ]
        for d in items:
            seed = d.pop('seed')
            img = _img(seed, 'team', 300, 300)
            obj = TeamMember(**d)
            if img:
                obj.image = img
            obj.save()
        self.stdout.write(f'  Created {len(items)} team members.')

    def _gallery(self):
        items = [
            {'title_ar': 'حفل افتتاح العام الدراسي',  'title_en': 'Academic Year Opening Ceremony',   'category': 'events',       'seed': 'lrc_gal_1'},
            {'title_ar': 'ورشة اللغة الإنجليزية',      'title_en': 'English Language Workshop',        'category': 'workshops',    'seed': 'lrc_gal_2'},
            {'title_ar': 'أسبوع الثقافة الفرنسية',     'title_en': 'French Culture Week',              'category': 'events',       'seed': 'lrc_gal_3'},
            {'title_ar': 'مسابقة الخطابة',              'title_en': 'Oratory Competition',              'category': 'competitions', 'seed': 'lrc_gal_4'},
            {'title_ar': 'زيارة الوفود الدولية',        'title_en': 'International Delegations Visit',  'category': 'events',       'seed': 'lrc_gal_5'},
            {'title_ar': 'دورة الترجمة الأدبية',        'title_en': 'Literary Translation Course',      'category': 'workshops',    'seed': 'lrc_gal_6'},
            {'title_ar': 'يوم اللغات العالمي',          'title_en': 'World Languages Day',              'category': 'events',       'seed': 'lrc_gal_7'},
            {'title_ar': 'فريق المركز',                 'title_en': 'Center Team',                      'category': 'team',         'seed': 'lrc_gal_8'},
        ]
        created = 0
        for d in items:
            seed = d.pop('seed')
            img = _img(seed, 'gallery', 600, 450)
            if img:
                GalleryImage.objects.create(image=img, **d)
                created += 1
        self.stdout.write(f'  Created {created} gallery images.')

    def _pages(self):
        items = [
            {
                'title_ar': 'عن المركز',
                'title_en': 'About the Center',
                'slug': 'about',
                'nav_order': 1,
                'content_ar': (
                    'مركز الموارد اللغوية في جامعة النجاح الوطنية هو مرجع أكاديمي متخصص في تعليم اللغات '
                    'وتنمية مهارات التواصل. أُسِّس المركز بهدف توفير بيئة تعليمية احترافية تُمكّن الطلبة '
                    'وأعضاء هيئة التدريس وأبناء المجتمع من اكتساب مهارات لغوية متقدمة في اللغات الإنجليزية '
                    'والفرنسية والألمانية والإسبانية وغيرها.\n\n'
                    'يضم المركز نخبة من الأساتذة والمدربين الحاملين لشهادات دولية معتمدة، ويقدم مجموعة '
                    'واسعة من البرامج التدريبية المصممة وفق أحدث الأساليب التربوية العالمية.'
                ),
                'content_en': (
                    'The Language Resource Center at An-Najah National University is a specialized academic '
                    'hub for language education and communication skill development. Established to provide '
                    'a professional learning environment, the Center enables students, faculty, and community '
                    'members to acquire advanced language skills in English, French, German, Spanish, and more.\n\n'
                    'The Center is staffed by qualified instructors holding internationally accredited '
                    'certificates, and offers a wide range of training programs designed according to the '
                    'latest global educational methodologies.'
                ),
            },
            {
                'title_ar': 'خدماتنا',
                'title_en': 'Our Services',
                'slug': 'services',
                'nav_order': 2,
                'content_ar': (
                    '<p>يقدّم مركز الموارد اللغوية مجموعة متنوعة من الخدمات اللغوية والأكاديمية:</p>'
                    '<ul>'
                    '<li>دورات اللغة الإنجليزية بمستوياتها المختلفة (مبتدئ، متوسط، متقدم)</li>'
                    '<li>دورات الفرنسية والألمانية والإسبانية</li>'
                    '<li>التحضير لاختبارات اللغة الدولية (IELTS, TOEFL, DELF, Goethe)</li>'
                    '<li>تدريب على مهارات الخطابة والتقديم</li>'
                    '<li>ورشات الكتابة الأكاديمية</li>'
                    '<li>برامج الترجمة والتعريب</li>'
                    '<li>برامج التبادل الثقافي والفعاليات الدولية</li>'
                    '</ul>'
                ),
                'content_en': (
                    '<p>The Language Resource Center offers a diverse range of linguistic and academic services:</p>'
                    '<ul>'
                    '<li>English language courses at all levels (beginner, intermediate, advanced)</li>'
                    '<li>French, German, and Spanish courses</li>'
                    '<li>International language test preparation (IELTS, TOEFL, DELF, Goethe)</li>'
                    '<li>Public speaking and presentation skills training</li>'
                    '<li>Academic writing workshops</li>'
                    '<li>Translation and localization programs</li>'
                    '<li>Cultural exchange programs and international events</li>'
                    '</ul>'
                ),
            },
        ]
        banners = [
            _img('lrc_page_about',    'pages', 1400, 600),
            _img('lrc_page_services', 'pages', 1400, 600),
        ]
        for d, banner in zip(items, banners):
            if banner:
                d['banner_image'] = banner
            Page.objects.create(**d)
        self.stdout.write(f'  Created {len(items)} pages.')
