"""
Creates locale/ar/LC_MESSAGES/django.mo without needing system gettext.
Run once: python manage.py setup_arabic
"""
import os
import struct

from django.conf import settings
from django.core.management.base import BaseCommand

TRANSLATIONS = {
    # ── Site-wide ──────────────────────────────────────────────────────
    'Language Resource Center':          'مركز الموارد اللغوية',
    'An-Najah National University':      'جامعة النجاح الوطنية',
    'Nablus, Palestine':                 'نابلس، فلسطين',
    'Nablus, West Bank, Palestine':      'نابلس، الضفة الغربية، فلسطين',
    'Home':                              'الرئيسية',
    'News':                              'الأخبار',
    'Gallery':                           'معرض الصور',
    'Stories':                           'قصص النجاح',
    'Team':                              'الفريق',
    'Contact':                           'تواصل معنا',
    'Contact Us':                        'تواصل معنا',
    'Pages':                             'الصفحات',
    'Visit Website':                     'زيارة الموقع',
    'All rights reserved':               'جميع الحقوق محفوظة',
    'Promoting language learning and cultural exchange at An-Najah National University, Nablus, Palestine.':
        'تعزيز تعلّم اللغات وتبادل الثقافات في جامعة النجاح الوطنية، نابلس، فلسطين.',
    'An-Najah National University is one of the largest universities in Palestine.':
        'جامعة النجاح الوطنية إحدى أكبر الجامعات في فلسطين.',

    # ── Home ───────────────────────────────────────────────────────────
    'Featured':                          'مميّز',
    'Latest News':                       'آخر الأخبار',
    'All News':                          'جميع الأخبار',
    'Read More':                         'اقرأ المزيد',
    'Read Full Article':                 'اقرأ المقال كاملاً',
    'Announcements':                     'الإعلانات',
    'No news published yet.':            'لا توجد أخبار منشورة بعد.',
    'No announcements at this time.':    'لا توجد إعلانات في الوقت الحالي.',
    'Photo Gallery':                     'معرض الصور',
    'View Gallery':                      'عرض المعرض',
    'Success Stories':                   'قصص النجاح',
    'All Stories':                       'جميع القصص',

    # ── News ───────────────────────────────────────────────────────────
    'Back to News':                      'العودة إلى الأخبار',

    # ── Gallery ────────────────────────────────────────────────────────
    'No images in the gallery yet.':     'لا توجد صور في المعرض بعد.',

    # ── Stories ────────────────────────────────────────────────────────
    'No stories yet.':                   'لا توجد قصص بعد.',

    # ── Team ───────────────────────────────────────────────────────────
    'Our Team':                          'فريقنا',
    'Team members coming soon.':         'أعضاء الفريق قريباً.',

    # ── Contact ────────────────────────────────────────────────────────
    'Get in Touch':                      'تواصل معنا',
    'Address':                           'العنوان',
    'Email':                             'البريد الإلكتروني',
    'Phone':                             'الهاتف',
    'Office Hours':                      'ساعات العمل',
    'Sunday – Thursday':            'الأحد – الخميس',
    'Full Name':                         'الاسم الكامل',
    'Email Address':                     'البريد الإلكتروني',
    'Subject':                           'الموضوع',
    'Message':                           'الرسالة',
    'Send Message':                      'إرسال الرسالة',
    'Thank you for your message. We will get back to you soon.':
        'شكراً لرسالتك. سنتواصل معك قريباً.',

    # ── Redesign strings ───────────────────────────────────────────────
    'Unlocking Global Communication':       'فتح آفاق التواصل العالمي',
    'Empowering students in high-quality language programs that connect cultures, build skills, and open doors to global opportunities.':
        'نُمكِّن الطلبة من الالتحاق ببرامج لغوية متميزة تجسر الثقافات وتبني المهارات وتفتح أبواب الفرص العالمية.',
    'Explore Programs':                     'استكشف البرامج',
    'Meet Our Team':                        'تعرّف على فريقنا',
    'Apply Now':                            'سجّل الآن',
    'Students Enrolled':                    'طالب ملتحق',
    'Languages Taught':                     'لغة مُدرَّسة',
    'Programs Offered':                     'برنامج متاح',
    'Alumni':                               'خريج',
    'Student Voices':                       'أصوات الطلبة',
    'Languages We Teach':                   'اللغات التي نُدرِّسها',
    'Language Program':                     'برنامج لغوي',
    'English Language':                     'اللغة الإنجليزية',
    'French Language':                      'اللغة الفرنسية',
    'More Languages':                       'لغات أخرى',
    'Explore':                              'استكشف',
    'Join Our Language Community':          'انضم إلى مجتمعنا اللغوي',
    'Whether you are a student looking to master a new language or a professional seeking excellence, our team is here to help.':
        'سواء كنت طالباً يسعى لإتقان لغة جديدة أم محترفاً يبحث عن التميز، فريقنا جاهز لمساعدتك.',
    'Contact Faculty':                      'تواصل مع الكادر',
    'Need Help?':                           'هل تحتاج مساعدة؟',
    'Our team is here to guide you through our programs and services.':
        'فريقنا جاهز لإرشادك عبر برامجنا وخدماتنا.',
    'Contact Us':                           'تواصل معنا',
    'Our Distinguished Faculty':            'أعضاء هيئة التدريس المتميزون',
    'A passionate group of world-class educators and administrators dedicated to fostering cross-cultural understanding through inspired language learning.':
        'مجموعة متميزة من المعلمين والإداريين ذوي المستوى العالمي، يكرسون جهودهم لتعزيز التفاهم عبر الثقافات من خلال تعليم اللغات.',
    'Leadership':                           'القيادة',
    'Director':                             'المدير',
    'Academic Staff':                       'الكادر الأكاديمي',
    'Visual Journey':                       'رحلة بصرية',
    'Explore the vibrant community, modern facilities, and cultural exchanges that define the Language Resource Center at An-Najah.':
        'استكشف المجتمع النابض والمرافق الحديثة وتبادل الثقافات التي تميز مركز الموارد اللغوية في جامعة النجاح.',
    'All':                                  'الكل',
    'Filter by Category':                   'تصفية حسب الفئة',
    'Have questions about our language programs? We\'re here to help you bridge cultural gaps and master new skills.':
        'هل لديك أسئلة حول برامجنا اللغوية؟ نحن هنا لمساعدتك على تجاوز الحواجز الثقافية وإتقان مهارات جديدة.',
    'Send us a Message':                    'أرسل لنا رسالة',
    'Direct Contact':                       'التواصل المباشر',
    'Follow Our Journey':                   'تابعنا',
    'Latest News':                          'آخر الأخبار',
    'Digital Resource Library':             'مكتبة الموارد الرقمية',
    'Access our collection of language learning materials, exercises, and recordings.':
        'استعرض مجموعتنا من المواد التعليمية والتمارين والتسجيلات اللغوية.',
    'Learn More':                           'اعرف أكثر',
    'Quick Links':                          'روابط سريعة',
    'Resources':                            'موارد',
    'University Portal':                    'بوابة الجامعة',
    'No stories yet.':                      'لا توجد قصص بعد.',
    'Language Resource Center — An-Najah National University':
        'مركز الموارد اللغوية — جامعة النجاح الوطنية',

    # ── Events ─────────────────────────────────────────────────────────
    'Events':                               'الفعاليات',
    'Event':                                'فعالية',
    'Annual Event':                         'فعالية سنوية',
    'View Details':                         'عرض التفاصيل',
    'No events yet.':                       'لا توجد فعاليات بعد.',
    'Discover our events that bring cultures together and empower students through language and dialogue.':
        'اكتشف فعالياتنا التي تجمع الثقافات وتمكّن الطلبة من خلال اللغة والحوار.',
    'About the Event':                      'عن الفعالية',
    'Cultural Booths':                      'الأجنحة الثقافية',
    'Interactive booths representing cultures and languages from around the world.':
        'أجنحة تفاعلية تمثل ثقافات ولغات من حول العالم.',
    'Live Performances':                    'عروض حية',
    'Student-led cultural performances and educational engagement activities.':
        'عروض ثقافية يقودها الطلبة وأنشطة تعليمية تفاعلية.',
    'Language Passport':                    'جواز السفر اللغوي',
    'A gamified exploration experience where visitors collect stamps from each cultural booth.':
        'تجربة استكشافية تفاعلية يجمع فيها الزوار طوابع من كل جناح ثقافي.',
    'Youth Empowerment':                    'تمكين الشباب',
    'Building 21st-century skills: intercultural communication, openness, and global awareness.':
        'بناء مهارات القرن الحادي والعشرين: التواصل بين الثقافات والانفتاح والوعي العالمي.',
    'What our participants say':            'ماذا يقول المشاركون',
    'Our Sponsors':                         'رعاتنا',
    'We thank our partners for making Language Open Day possible.':
        'نشكر شركاءنا الذين يجعلون يوم اللغات المفتوح ممكناً.',
    'Want to Participate?':                 'هل تريد المشاركة؟',
    'Whether as a student, sponsor, or partner — join us in making the next event even bigger.':
        'سواء كنت طالباً أو راعياً أو شريكاً — انضم إلينا لجعل الفعالية القادمة أكبر.',

    # ── Contact form placeholders ──────────────────────────────────────
    'Enter your name':                      'أدخل اسمك',
    'Enter your email':                     'أدخل بريدك الإلكتروني',
    'What is this about?':                  'ما هو الموضوع؟',
    'Write your message here...':           'اكتب رسالتك هنا...',

    # ── Pages ──────────────────────────────────────────────────────────
    'Interested in our programs?':          'مهتم ببرامجنا؟',
    'Contact us today to learn more about enrollment and available courses.':
        'تواصل معنا اليوم لمعرفة المزيد عن التسجيل والدورات المتاحة.',
    'Location':                             'الموقع',

    # ── News list ──────────────────────────────────────────────────────
    'Stay updated with the latest news, events, and achievements from the Language Resource Center.':
        'تابع آخر الأخبار والفعاليات والإنجازات من مركز الموارد اللغوية.',

    # ── Stories ────────────────────────────────────────────────────────
    'Real stories from our students who transformed their lives through language learning.':
        'قصص حقيقية من طلبتنا الذين غيّروا حياتهم من خلال تعلم اللغات.',
    'Share Your Story':                     'شارك قصتك',
    'Have a success story to share? We\'d love to hear how the LRC helped you achieve your goals.':
        'لديك قصة نجاح؟ يسعدنا سماع كيف ساعدك المركز في تحقيق أهدافك.',
}


def _write_mo(translations, path):
    """Write a GNU .mo binary without requiring system gettext."""
    entries = {
        '': (
            'Content-Type: text/plain; charset=UTF-8\n'
            'Content-Transfer-Encoding: 8bit\n'
        )
    }
    entries.update(translations)

    keys = sorted(entries.keys())
    n = len(keys)

    ORIG_TBL  = 28
    TRAN_TBL  = ORIG_TBL + n * 8
    STR_START = TRAN_TBL + n * 8

    orig_enc = [k.encode('utf-8') for k in keys]
    tran_enc = [entries[k].encode('utf-8') for k in keys]

    orig_block = b''
    orig_off = []
    for s in orig_enc:
        orig_off.append((len(s), STR_START + len(orig_block)))
        orig_block += s + b'\x00'

    tran_block = b''
    tran_off = []
    tran_base = STR_START + len(orig_block)
    for s in tran_enc:
        tran_off.append((len(s), tran_base + len(tran_block)))
        tran_block += s + b'\x00'

    buf = bytearray()
    buf += struct.pack('<IIIIIII', 0x950412de, 0, n, ORIG_TBL, TRAN_TBL, 0, 0)
    for length, offset in orig_off:
        buf += struct.pack('<II', length, offset)
    for length, offset in tran_off:
        buf += struct.pack('<II', length, offset)
    buf += orig_block
    buf += tran_block

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(buf)


class Command(BaseCommand):
    help = 'Generate Arabic .mo translation file (no system gettext required)'

    def handle(self, *args, **options):
        mo_path = os.path.join(
            settings.BASE_DIR, 'locale', 'ar', 'LC_MESSAGES', 'django.mo'
        )
        _write_mo(TRANSLATIONS, mo_path)
        self.stdout.write(self.style.SUCCESS(
            f'Arabic .mo file written ({len(TRANSLATIONS)} strings) -> {mo_path}'
        ))
