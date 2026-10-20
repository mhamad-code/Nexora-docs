import re, os, shutil, json, zipfile, html as H
from xml.dom import minidom

SRC = '/home/claude/site'; OUT = '/home/claude/out'
SITE = 'https://mhamad-code.github.io/Nexora-docs'   # غيّره إلى دومينك الفعلي
DEV_EN, DEV_AR, DEV_URL = 'Mohamed Hamra', 'محمد حمرة', 'https://github.com/mhamad-code'
TODAY = '2026-10-20'
shutil.rmtree(OUT, ignore_errors=True); shutil.copytree(SRC, OUT)
os.makedirs(OUT + '/ar', exist_ok=True)
rd = lambda p: open(p, encoding='utf8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf8').write(s)
q = lambda s: H.escape(s, quote=True)

# ---------- Arabic content ----------
def card(h, t, b, ext=False):
    e = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="card link" href="{h}"{e}><div class="card-t">{t}</div><div class="card-b"><p>{b}</p></div><span class="card-go">←</span></a>'
def co(k, t): return f'<div class="callout {k}"><div class="co-ic">{ {"note":"ℹ️","tip":"💡","warning":"⚠️"}[k] }</div><div class="co-b">{t}</div></div>'
def step(t, b): return f'<div class="step"><div class="step-t">{t}</div><div class="step-b">{b}</div></div>'
REL = 'https://github.com/mhamad-code/Nexora/releases/tag/latest'

INTRO = ('<p>يجمع Nexora كل مزوّدي الذكاء الاصطناعي الكبار في تطبيق أندرويد واحد متقن. بدل التنقل بين تطبيقات وتبويبات متصفح متعددة، تربط مفاتيح API الخاصة بك مرة واحدة وتتحدث مع OpenAI وGoogle Gemini وAnthropic Claude أو أي واجهة متوافقة مع OpenAI من الواجهة المألوفة نفسها. بُني Nexora بلغة Kotlin وJetpack Compose، فيبدو سريعًا وسلسًا ومنسجمًا تمامًا مع جهازك.</p>'
 '<h2 id="get-started">ابدأ من هنا</h2><div class="cards cols-2">'
 + card('download.html', 'تنزيل Nexora', 'ثبّت Nexora من صفحة الإصدارات على GitHub وابدأ خلال دقائق.')
 + card('quickstart.html', 'البدء السريع', 'أضف أول مزوّد، واختر نموذجًا، وأرسل أول رسالة في أقل من خمس دقائق.')
 + card('../providers/overview.html', 'مزوّدو الذكاء الاصطناعي', 'اربط OpenAI وGoogle Gemini وAnthropic Claude أو أي واجهة API متوافقة مع OpenAI.')
 + card('../assistants/overview.html', 'المساعدون', 'أنشئ مساعدين مخصصين بتعليمات نظام ونماذج وشخصيات خاصة بك.')
 + card('../extensions/mcp.html', 'إضافات MCP', 'وسّع إمكانيات Nexora عبر أدوات بروتوكول سياق النموذج (MCP).')
 + card('../settings/web-access.html', 'الوصول عبر الويب', 'افتح واجهة محادثة Nexora من متصفح على شبكتك المحلية.')
 + '</div><h2 id="why-nexora">لماذا Nexora؟</h2><p>صُمم Nexora حول فكرة واحدة: تجربتك مع الذكاء الاصطناعي يجب أن تكون ملكك. تستخدم مفاتيح API الخاصة بك، وتختار نماذجك، وتحتفظ بخصوصية محادثاتك. بلا اشتراكات ولا وسطاء ولا قيود على الانتقال.</p><div class="cards cols-2">'
 + card('../providers/overview.html', 'مزوّدون متعددون في تطبيق واحد', 'بدّل بين OpenAI وGemini وClaude والواجهات المتوافقة دون مغادرة التطبيق.')
 + card('../assistants/overview.html', 'مساعدون مخصصون', 'ابنِ مساعدين قابلين لإعادة الاستخدام بتعليمات نظام ونماذج وشخصيات مختلفة.')
 + card('../extensions/mcp.html', 'دعم أدوات MCP', 'اربط أدوات ومصادر بيانات خارجية عبر بروتوكول سياق النموذج.')
 + card('../chat/search.html', 'بحث مباشر على الويب', 'فعّل الوصول اللحظي للويب لتبقى إجابات الذكاء الاصطناعي دقيقة وحديثة.')
 + '</div><hr><p>يستند Nexora إلى <a href="https://github.com/rikkahub/rikkahub">RikkaHub</a> (رخصة AGPL-3.0). هذا التوثيق مقتبس من توثيق RikkaHub المنشور برخصة MIT — راجع <a href="https://github.com/mhamad-code/Nexora-docs/blob/main/LICENSE">LICENSE</a>.</p>')

DOWNLOAD = ('<p>Nexora تطبيق أندرويد أصلي يُوزَّع كملف APK من صفحة إصدارات المشروع على GitHub. تشرح لك هذه الصفحة التنزيل والتثبيت وإكمال أول تشغيل.</p>'
 '<h2 id="system-requirements">متطلبات النظام</h2>' + co('note', '<p>يعمل Nexora على هواتف وأجهزة أندرويد اللوحية. لا توجد نسخة لنظام iOS.</p>')
 + '<h2 id="download">التنزيل</h2><div class="steps">'
 + step('افتح صفحة الإصدارات', f'<p>اذهب في متصفحك إلى <strong><a href="{REL}">صفحة إصدارات Nexora</a></strong>.</p>')
 + step('اختر الملف المناسب', '<p>يحتوي كل إصدار على عدة ملفات APK:</p><table><thead><tr><th>الملف</th><th>متى تستخدمه</th></tr></thead><tbody>'
   '<tr><td><code>app-arm64-v8a-release.apk</code></td><td>معظم الهواتف الحديثة (معالج 64 بت).</td></tr>'
   '<tr><td><code>app-armeabi-v7a-release.apk</code></td><td>الهواتف الأقدم ذات المعالج 32 بت.</td></tr>'
   '<tr><td><code>app-x86_64-release.apk</code></td><td>المحاكيات والأجهزة ذات شريحة x86.</td></tr>'
   '<tr><td><code>app-universal-release.apk</code></td><td>يعمل على كل ما سبق، لكن حجم الملف أكبر.</td></tr></tbody></table>'
   '<p>إذا لم تكن متأكدًا من الملف المناسب لجهازك، فاستخدم النسخة الشاملة (universal).</p>')
 + step('ثبّت ملف APK', '<p>افتح الملف الذي نزّلته من مدير الملفات. إذا طُلب منك ذلك، فعّل <strong>Install unknown apps</strong> للمتصفح أو مدير الملفات، ثم اتبع التعليمات على الشاشة.</p>')
 + '</div>' + co('warning', '<p>نزّل Nexora من المستودع الرسمي المذكور أعلاه فقط. ملفات APK من مصادر أخرى قد تكون قديمة أو معدّلة.</p>')
 + co('note', '<p>للتحديث، ثبّت ملف APK أحدث فوق التطبيق الحالي. الإصدارات موقّعة بالمفتاح نفسه، لذا تبقى بياناتك محفوظة.</p>')
 + '<h2 id="first-launch-experience">تجربة أول تشغيل</h2><p>بعد تثبيت Nexora افتحه من الشاشة الرئيسية أو قائمة التطبيقات. في أول تشغيل يرشدك Nexora خلال الإعدادات الأساسية:</p><div class="steps">'
 + step('شاشة الترحيب', '<p>يستقبلك Nexora بشاشة ترحيب قصيرة. اضغط <strong>Get Started</strong> للانتقال إلى الإعداد.</p>')
 + step('أضف مزوّدًا', '<p>يطلب منك Nexora إضافة مزوّد ذكاء اصطناعي واحد على الأقل. اختر مزوّدك المفضل — OpenAI أو Google Gemini أو Anthropic Claude أو واجهة مخصصة متوافقة مع OpenAI — وأدخل مفتاح API. يمكنك إضافة مزوّدين آخرين لاحقًا من <strong>Settings ← Providers</strong>.</p>')
 + step('اختر نموذجًا افتراضيًا', '<p>اختر نموذجًا افتراضيًا للمحادثات الجديدة. يمكنك تغيير النموذج لكل محادثة في أي وقت.</p>')
 + step('ابدأ الدردشة', '<p>اضغط <strong>Start Chatting</strong> لفتح شاشة المحادثة الرئيسية. Nexora جاهز للاستخدام.</p>')
 + '</div><h2 id="import-provider-settings-via-qr-code">استيراد إعدادات المزوّد عبر رمز QR</h2><p>إذا كنت قد هيّأت Nexora على جهاز آخر، فيمكنك تخطي إدخال مفاتيح API يدويًا باستيراد إعدادات المزوّد برمز QR.</p>'
 '<details class="acc"><summary>كيفية الاستيراد عبر رمز QR</summary><div class="acc-b"><p>على جهازك الحالي:</p><ol>'
 '<li>افتح <strong>Settings ← Providers</strong>.</li><li>اضغط خيار <strong>Export</strong> أو <strong>Share</strong> واختر <strong>QR Code</strong>.</li><li>سيظهر على الشاشة رمز QR يحتوي إعدادات المزوّد.</li></ol>'
 '<p>على جهازك الجديد:</p><ol><li>أكمل التثبيت وافتح Nexora.</li><li>في شاشة إعداد المزوّد اضغط <strong>Import via QR Code</strong>.</li><li>وجّه الكاميرا إلى رمز QR على جهازك الحالي.</li><li>يستورد Nexora إعدادات المزوّد تلقائيًا.</li></ol>'
 + co('note', '<p>يتضمن رمز QR مفاتيح API الخاصة بك. أبقِه سريًا ولا تشاركه علنًا ولا تلتقط له لقطة شاشة وتحفظها في مكان غير آمن.</p>') + '</div></details>'
 '<h2 id="next-steps">الخطوات التالية</h2><div class="cards cols-2">'
 + card('quickstart.html', 'دليل البدء السريع', 'أضف مزوّدًا وأرسل أول رسالة في أقل من خمس دقائق.')
 + card('../providers/overview.html', 'نظرة عامة على المزوّدين', 'تعرّف على إعداد OpenAI وGemini وClaude والواجهات المخصصة.') + '</div>')

QUICK = ('<p>يوصلك هذا الدليل من الصفر إلى أول محادثة مع الذكاء الاصطناعي بأسرع طريقة. تحتاج إلى جهاز أندرويد مثبّت عليه Nexora ومفتاح API من مزوّد واحد على الأقل. إذا لم يكن لديك مفتاح بعد، فسجّل لدى المزوّد الذي تختاره أولًا.</p><div class="steps">'
 + step('نزّل Nexora وثبّته', '<p>ثبّت Nexora على جهاز أندرويد من صفحة الإصدارات على GitHub.</p>' + card(REL, 'إصدارات Nexora (GitHub)', 'نزّل أحدث ملف APK من صفحة إصدارات المشروع.', True) + '<p>بعد اكتمال التثبيت افتح Nexora من الشاشة الرئيسية أو قائمة التطبيقات.</p>')
 + step('افتح الإعدادات وأضف مزوّدًا', '<p>يحتاج Nexora إلى مزوّد ذكاء اصطناعي واحد على الأقل قبل أن تتمكن من الدردشة. انتقل إلى إعدادات المزوّدين الآن.</p><ol>'
   '<li>اضغط أيقونة <strong>Settings</strong> (الترس) أسفل الشريط الجانبي.</li><li>اختر <strong>Provider Settings</strong> من قائمة الإعدادات.</li>'
   '<li>كثير من المزوّدين مهيّؤون مسبقًا — إن وجدت مزوّدك فاضغط عليه وأدخل مفتاح API. وإلا فاضغط الزر في الزاوية العلوية لإنشاء مزوّد جديد.</li></ol>'
   '<div class="tabs"><div class="tab-bar" role="tablist"><button role="tab" class="tab-btn on">OpenAI</button><button role="tab" class="tab-btn">Google Gemini</button><button role="tab" class="tab-btn">Anthropic Claude</button></div>'
   '<div class="tab-panel on" role="tabpanel"><p>أكثر صيغ API انتشارًا. أدخل عنوان Base URL ومفتاح API من مزوّدك لإكمال الإعداد.</p><p>لدى OpenAI إصداران من API. <strong>Chat Completions</strong> هو الافتراضي في Nexora وهو الأكثر شيوعًا وتدعمه غالبية المزوّدين. أما <strong>Responses API</strong> الأحدث فهو ما تمنحه OpenAI الأولوية الآن — فإذا كنت تستخدم واجهة OpenAI الرسمية أو وسيطًا يحاكي نماذج GPT فيُنصح بالتحويل إليه. اضغط <strong>Use Responses API</strong> لتفعيله.</p></div>'
   '<div class="tab-panel" role="tabpanel"><p>صيغة API الخاصة بـ Google، وتُستخدم حصريًا مع نماذج Google Gemini.</p></div>'
   '<div class="tab-panel" role="tabpanel"><p>ثاني أكثر صيغ API اعتمادًا بعد OpenAI. يستخدمها Claude وعدد من النماذج الأخرى أيضًا.</p></div></div>')
 + step('أدخل مفتاح API', '<p>الصق مفتاح API في حقل <strong>API Key</strong> للمزوّد الذي اخترته.</p><p>إذا كنت تستخدم وسيطًا غير رسمي وغير مدمج في Nexora، فستحتاج أيضًا إلى ضبط <strong>Base URL</strong> عند إنشاء المزوّد.</p>'
   + co('warning', '<p>تعامل مع مفتاح API كأنه كلمة مرور. لا تشاركه ولا تلصقه في تطبيقات غير موثوقة. يحفظ Nexora مفتاحك محليًا على جهازك ولا يرسله أبدًا إلى خوادم Nexora — بل يذهب مباشرة إلى المزوّد الذي اخترته.</p>') + '<p>بعد لصق المفتاح اضغط <strong>Save</strong> أو <strong>Confirm</strong> لحفظ إعدادات المزوّد.</p>')
 + step('أضف النماذج', '<p>بعد ضبط المزوّد، مرّر إلى قسم <strong>Models</strong> أسفل شاشة المزوّد واضغط عليه.</p><p>يدعم معظم المزوّدين جلب قائمة النماذج تلقائيًا — اضغط زر التوسيع لتحميل القائمة ثم اختر النماذج التي تريدها.</p><p>لحذف نموذج لم تعد بحاجة إليه، اسحبه للحذف.</p>'
   + co('note', '<p>يمكنك تغيير النموذج في أي وقت من داخل المحادثة عبر منتقي النموذج في شريط أدوات الدردشة.</p>'))
 + step('اضبط النماذج الافتراضية', '<p>ارجع إلى صفحة الإعدادات واختر <strong>Default Models &amp; Prompts</strong> لتحديد النموذج الافتراضي لكل ميزة.</p><p>إلى جانب نموذج الدردشة، يمكن لميزات أخرى (مثل توليد العناوين والتلخيص) أن تستخدم كل منها نموذجًا مختلفًا — وغالبًا ما يؤدي نموذج أسرع وأرخص عملًا جيدًا في هذه المهام.</p>')
 + step('ابدأ أول محادثة', '<p>كل شيء جاهز. ارجع إلى الشاشة الرئيسية وابدأ محادثة جديدة.</p><ol><li>اضغط زر اختيار النموذج أسفل الشاشة لاختيار النموذج الذي تريده.</li><li>اكتب رسالتك الأولى في حقل النص واضغط <strong>Send</strong>.</li></ol><p>يبثّ Nexora الرد إليك لحظة بلحظة. هذا كل شيء — أنت جاهز!</p>'
   + co('tip', '<p>جرّب بداية بسيطة مثل <em>«اشرح لي ما الذي يمكنك مساعدتي فيه»</em> لتتعرف على قدرات النموذج قبل الانتقال إلى مهام أكثر تحديدًا.</p>')
   + co('warning', '<p>تجنّب سؤال النموذج عن هويته. فالنماذج لا تملك وعيًا دقيقًا بهويتها — وهذه خاصية أساسية في طريقة عمل النماذج اللغوية الكبيرة وليست خللًا في Nexora.</p><p>تستطيع التطبيقات الرسمية الإجابة بشكل صحيح لأنها تحقن تعليمات نظام تخبر النموذج بهويته. لا يتضمن Nexora هذه التعليمات افتراضيًا، لكن يمكنك إضافتها بنفسك من إعدادات تعليمات النظام.</p>'))
 + '</div><h2 id="what-to-explore-next">ماذا تستكشف بعد ذلك</h2><div class="cards cols-2">'
 + card('../providers/overview.html', 'نظرة عامة على المزوّدين', 'أضف مزوّدين آخرين وتعلّم الخيارات المتقدمة مثل عناوين Base URL والترويسات المخصصة.')
 + card('../assistants/overview.html', 'المساعدون المخصصون', 'أنشئ مساعدين قابلين لإعادة الاستخدام بتعليمات نظام ونماذج افتراضية وشخصيات خاصة.')
 + card('../extensions/mcp.html', 'إضافات MCP', 'اربط أدوات ومصادر بيانات خارجية ليتمكن الذكاء الاصطناعي من تنفيذ إجراءات حقيقية.')
 + card('../settings/web-access.html', 'الوصول عبر الويب', 'فعّل البحث المباشر على الويب ليجيب الذكاء الاصطناعي عن الأحداث والمعلومات الحديثة.') + '</div>')

AR = {
 'introduction.html': dict(title='مرحبًا بك في Nexora — تطبيق دردشة بالذكاء الاصطناعي لأندرويد', eyebrow='ابدأ من هنا', body=INTRO,
   desc='Nexora تطبيق أندرويد أصلي يجمع OpenAI وGoogle Gemini وAnthropic Claude وأي مزوّد متوافق مع OpenAI في واجهة واحدة أنيقة.', prev=None, next=('download.html', 'التنزيل')),
 'download.html': dict(title='تثبيت Nexora على أندرويد', eyebrow='ابدأ من هنا', body=DOWNLOAD,
   desc='نزّل ملف Nexora APK من إصدارات GitHub، واختر النسخة المناسبة لجهازك، وأكمل إعداد أول تشغيل.', prev=('introduction.html', 'المقدمة'), next=('quickstart.html', 'البدء السريع')),
 'quickstart.html': dict(title='البدء السريع: أرسل أول رسالة للذكاء الاصطناعي في 5 دقائق', eyebrow='ابدأ من هنا', body=QUICK,
   desc='ثبّت Nexora على أندرويد، واربط أول مزوّد ذكاء اصطناعي بمفتاح API الخاص بك، واختر نموذجًا، وأرسل أول رسالة في أقل من خمس دقائق.', prev=('download.html', 'التنزيل'), next=('../providers/overview.html', 'نظرة عامة على المزوّدين (EN)')),
}
NAV = [('ابدأ من هنا', [('المقدمة', 'introduction.html'), ('التنزيل', 'download.html'), ('البدء السريع', 'quickstart.html')]),
 ('المزوّدون', [('نظرة عامة', 'providers/overview.html'), ('OpenAI', 'providers/openai.html'), ('Google', 'providers/google.html'), ('Claude', 'providers/claude.html'), ('مخصص', 'providers/custom.html')]),
 ('المحادثة', [('المحادثات', 'chat/conversations.html'), ('الوسائط المتعددة', 'chat/multimodal.html'), ('التفرّع', 'chat/branching.html'), ('البحث على الويب', 'chat/search.html')]),
 ('المساعدون', [('نظرة عامة', 'assistants/overview.html'), ('الذاكرة', 'assistants/memory.html'), ('حقن الأوامر', 'assistants/prompt-injection.html')]),
 ('الإضافات', [('MCP', 'extensions/mcp.html'), ('المهارات', 'extensions/skills.html'), ('مساحة العمل', 'extensions/workspace.html'), ('الصوت', 'extensions/speech.html'), ('توليد الصور', 'extensions/image-generation.html')]),
 ('الإعدادات والمزامنة', [('المظهر', 'settings/appearance.html'), ('الوصول عبر الويب', 'settings/web-access.html'), ('النسخ الاحتياطي', 'settings/backup.html')])]

# ---------- SEO helpers ----------
def url(p):
    if p in ('index.html', 'introduction.html'): return SITE + '/'
    if p in ('ar/index.html', 'ar/introduction.html'): return SITE + '/ar/'
    return SITE + '/' + p
def ar_of(p):
    if p == 'index.html': return 'ar/index.html'
    return 'ar/' + p if p in AR else None
def seo(p, lang, title, desc, alt_en, alt_ar, section):
    canon = url(p); ar = lang == 'ar'
    t = [f'<!-- Developed by {DEV_EN} ({DEV_AR}) — {DEV_URL} -->',
         '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">',
         f'<meta name="author" content="{DEV_EN} | {DEV_AR}">', f'<meta name="copyright" content="© 2026 {DEV_EN}">', '<meta name="theme-color" content="#4f46e5">',
         f'<link rel="canonical" href="{canon}">']
    if alt_en: t.append(f'<link rel="alternate" hreflang="en" href="{url(alt_en)}">')
    if alt_ar: t.append(f'<link rel="alternate" hreflang="ar" href="{url(alt_ar)}">')
    if alt_en: t.append(f'<link rel="alternate" hreflang="x-default" href="{url(alt_en)}">')
    t += [f'<link rel="sitemap" type="application/xml" href="{SITE}/sitemap.xml">', f'<link rel="alternate" type="text/plain" href="{SITE}/llms.txt" title="LLM-friendly index">',
          '<meta property="og:type" content="article">', '<meta property="og:site_name" content="Nexora Docs">', f'<meta property="og:title" content="{q(title)}">',
          f'<meta property="og:description" content="{q(desc)}">', f'<meta property="og:url" content="{canon}">', f'<meta property="og:locale" content="{"ar_AR" if ar else "en_US"}">',
          f'<meta property="og:locale:alternate" content="{"en_US" if ar else "ar_AR"}">', '<meta name="twitter:card" content="summary">', f'<meta name="twitter:title" content="{q(title)}">', f'<meta name="twitter:description" content="{q(desc)}">']
    person = {"@type": "Person", "name": DEV_EN, "alternateName": DEV_AR, "url": DEV_URL}
    home = SITE + ('/ar/' if ar else '/')
    g = [{"@type": "TechArticle", "headline": title, "description": desc, "inLanguage": lang, "url": canon, "dateModified": TODAY, "author": person,
          "publisher": {"@type": "Organization", "name": "Nexora", "url": home}, "isPartOf": {"@type": "WebSite", "name": "Nexora Docs", "url": home, "inLanguage": lang}},
         {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Nexora", "item": home}, {"@type": "ListItem", "position": 2, "name": section}, {"@type": "ListItem", "position": 3, "name": title}]}]
    if p in ('index.html', 'ar/index.html'):
        g.append({"@type": "SoftwareApplication", "name": "Nexora", "operatingSystem": "Android", "applicationCategory": "CommunicationApplication", "description": desc, "author": person,
                  "downloadUrl": REL, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "inLanguage": lang})
    t.append('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False).replace('</', '<\\/') + '</script>')
    return '\n'.join(t) + '\n'

# ---------- CSS / JS ----------
with open(OUT + '/assets/style.css', 'a', encoding='utf8') as f:
    f.write('\n.lang-btn{font-weight:600;font-size:13px;padding:6px 10px;border:1px solid var(--bd);border-radius:8px;color:var(--fg)!important;text-decoration:none!important;white-space:nowrap}'
            '\n.nav-link small{opacity:.55;font-size:10px;margin-inline-start:6px;font-weight:600}\n.foot a{color:inherit;font-weight:600;text-decoration:underline}\n')
wr(OUT + '/assets/rtl.css', '''html[dir=rtl] body{font-family:"Segoe UI",Tahoma,"Noto Sans Arabic","Noto Naskh Arabic",system-ui,-apple-system,sans-serif;line-height:1.9}
html[dir=rtl] .side{border-right:0;border-left:1px solid var(--bd);padding:26px 20px 40px 14px}
html[dir=rtl] .prose th,html[dir=rtl] .prose td{text-align:right}
html[dir=rtl] .prose blockquote{border-left:0;border-right:3px solid var(--bd)}
html[dir=rtl] .card-go{right:auto;left:16px}
html[dir=rtl] .steps{border-left:0;border-right:1px solid var(--bd);margin-left:0;margin-right:14px}
html[dir=rtl] .step{padding:0 34px 26px 0}
html[dir=rtl] .step:before{left:auto;right:-15px}
html[dir=rtl] .pn.next{text-align:left;margin-left:0;margin-right:auto}
html[dir=rtl] .toc .toc-3{padding-left:0;padding-right:14px}
html[dir=rtl] .search{margin:0 28px 0 auto}
html[dir=rtl] .prose ol,html[dir=rtl] .prose ul{padding-left:0;padding-right:1.4em}
html[dir=rtl] code,html[dir=rtl] pre,html[dir=rtl] kbd{direction:ltr;unicode-bidi:isolate;text-align:left}
html[dir=rtl] .acc summary{text-align:right}
@media(max-width:800px){html[dir=rtl] .side{left:auto;right:0;transform:translateX(100%);border-left:0;border-right:0}
html[dir=rtl] .side.open{transform:none}html[dir=rtl] .search{margin-right:0}}
''')
js = rd(OUT + '/assets/app.js'); old = "'<a><b>No results</b></a>'"; assert old in js
wr(OUT + '/assets/app.js', js.replace(old, "'<a><b>'+(window.NO_RES||'No results')+'</b></a>'"))

# ---------- English pages ----------
en_index = json.loads(re.sub(r'^window\.SEARCH_INDEX=|;\s*$', '', rd(OUT + '/assets/search-index.js')))
pages = []
for root, _, fs in os.walk(OUT):
    for fn in fs:
        if fn.endswith('.html') and '/ar' not in root.replace(OUT, '', 1)[:3]:
            pages.append(os.path.relpath(os.path.join(root, fn), OUT))
for p in sorted(pages):
    h = rd(f'{OUT}/{p}'); rel = '../' * p.count('/')
    title = re.search(r'<title>(.*?)</title>', h, re.S).group(1); desc = re.search(r'<meta name="description" content="(.*?)">', h).group(1)
    sec = re.search(r'<div class="eyebrow">(.*?)</div>', h).group(1); ap = ar_of(p)
    h = h.replace('</head>', seo(p, 'en', H.unescape(title), H.unescape(desc), p, ap, H.unescape(sec)) + '</head>', 1)
    h = h.replace('<button class="theme-btn"', f'<a class="lang-btn" href="{rel}{ap or "ar/index.html"}" hreflang="ar" lang="ar" title="النسخة العربية">العربية</a><button class="theme-btn"', 1)
    h = re.sub(r'<footer class="foot">.*?</footer>', f'<footer class="foot">Nexora documentation &middot; adapted from RikkaHub docs (MIT) &middot; &copy; 2026 Developed by <a href="{DEV_URL}" rel="author noopener" target="_blank">{DEV_EN}</a></footer>', h, flags=re.S)
    wr(f'{OUT}/{p}', h)

# ---------- Arabic pages ----------
base = rd(f'{SRC}/index.html')
hdr = re.search(r'<header class="top">.*?</header>', base, re.S).group(0)
hdr = hdr.replace('aria-label="Menu"', 'aria-label="القائمة"').replace('placeholder="Search docs..."', 'placeholder="ابحث في التوثيق..."').replace('aria-label="Toggle theme"', 'aria-label="تبديل المظهر"')
def nav(cur):
    o = ''
    for g, items in NAV:
        o += f'<div class="nav-group"><div class="nav-title">{g}</div>'
        for lbl, pth in items:
            done = pth in AR
            href = pth if done else '../' + pth
            act = ' active' if pth == cur else ''
            o += f'<a class="nav-link{act}" href="{href}"' + ('' if done else ' hreflang="en" lang="en"') + f'>{lbl}' + ('' if done else '<small>EN</small>') + '</a>'
        o += '</div>'
    return o
ar_index = []
def plain(s): return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
def build_ar(name, d, out_name):
    toc = ''.join(f'<a class="toc-2" href="#{i}">{plain(t)}</a>' for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', d['body']))
    pn = (f'<a class="pn prev" href="{d["prev"][0]}"><span>السابق</span>{d["prev"][1]}</a>' if d['prev'] else '<span></span>') + f'<a class="pn next" href="{d["next"][0]}"><span>التالي</span>{d["next"][1]}</a>'
    en_name = 'index.html' if out_name == 'index.html' else out_name
    hd = hdr.replace('<button class="theme-btn"', f'<a class="lang-btn" href="../{en_name}" hreflang="en" lang="en" title="English version">English</a><button class="theme-btn"', 1)
    ttl = d['title'] + ' - Nexora'; p = 'ar/' + out_name
    page = (f'<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{q(ttl)}</title>\n<meta name="description" content="{q(d["desc"])}">\n'
            '<script>try{var t=localStorage.getItem(\'theme\');if(t)document.documentElement.dataset.theme=t;}catch(e){}</script>\n<link rel="stylesheet" href="../assets/style.css">\n<link rel="stylesheet" href="../assets/rtl.css">\n'
            + seo(p, 'ar', ttl, d['desc'], en_name, p, d['eyebrow']) + f'</head>\n<body>\n{hd}\n<div class="layout">\n<nav class="side" id="side">{nav("introduction.html" if out_name == "index.html" else out_name)}</nav>\n'
            f'<main class="main">\n<div class="eyebrow">{d["eyebrow"]}</div>\n<h1 class="page-title">{d["title"]}</h1>\n<p class="page-desc">{d["desc"]}</p>\n<article class="prose">{d["body"]}</article>\n<div class="pn-row">{pn}</div>\n'
            f'<footer class="foot">توثيق Nexora &middot; مقتبس من توثيق RikkaHub (MIT) &middot; &copy; 2026 تطوير <a href="{DEV_URL}" rel="author noopener" target="_blank">{DEV_AR}</a></footer>\n</main>\n'
            f'<aside class="toc"><div class="toc-h">في هذه الصفحة</div>{toc}</aside>\n</div>\n<script>window.BASE="";window.NO_RES="لا توجد نتائج";</script>\n<script src="search-index.js"></script>\n<script src="../assets/app.js"></script>\n</body>\n</html>')
    wr(f'{OUT}/ar/{out_name}', page)
for name, d in AR.items():
    build_ar(name, d, name)
    ar_index.append(dict(t=d['title'], g=d['eyebrow'], u=name, d=d['desc'], x=plain(d['body'])))
build_ar('introduction.html', AR['introduction.html'], 'index.html')
wr(OUT + '/ar/search-index.js', 'window.SEARCH_INDEX=' + json.dumps(ar_index, ensure_ascii=False) + ';')

# ---------- sitemap / robots / llms / 404 ----------
entries = []
for p in sorted(pages):
    if p in ('introduction.html', '404.html'): continue
    entries.append((p, ar_of(p)))
for a in ('ar/download.html', 'ar/quickstart.html'): entries.append((a, None))
def entry(p, alt_en, alt_ar):
    pr = '1.0' if p in ('index.html', 'ar/index.html') else '0.9' if 'download' in p or 'quickstart' in p else '0.7'
    s = f'<url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority>'
    if alt_en and alt_ar:
        s += f'<xhtml:link rel="alternate" hreflang="en" href="{url(alt_en)}"/><xhtml:link rel="alternate" hreflang="ar" href="{url(alt_ar)}"/><xhtml:link rel="alternate" hreflang="x-default" href="{url(alt_en)}"/>'
    return s + '</url>'
rows = []
for p, a in entries:
    if p.startswith('ar/'): rows.append(entry(p, p[3:], p))
    else: rows.append(entry(p, p, a))
wr(OUT + '/sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(rows) + '\n</urlset>\n')
bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot', 'anthropic-ai', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'Bingbot', 'Googlebot', 'CCBot', 'Meta-ExternalAgent', 'DuckAssistBot', 'cohere-ai']
wr(OUT + '/robots.txt', '# Nexora docs — search engines and AI crawlers are welcome.\n# Developed by Mohamed Hamra (محمد حمرة) — ' + DEV_URL + '\nUser-agent: *\nAllow: /\n\n' + ''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots) + f'Sitemap: {SITE}/sitemap.xml\n')
wr(OUT + '/.nojekyll', '')
li = lambda items, pre: '\n'.join(f'- [{i["t"]}]({SITE}/{pre}{i["u"]}): {i["d"]}' for i in items if i['u'] != 'introduction.html' or pre)
en_main = [i for i in en_index]
wr(OUT + '/llms.txt', f'# Nexora Docs\n\n> Official documentation for Nexora, a native Android (Kotlin + Jetpack Compose) AI chat app that unifies OpenAI, Google Gemini, Anthropic Claude and any OpenAI-compatible provider. Bring your own API keys; no subscriptions. Documentation available in English and Arabic (العربية, RTL).\n\nDeveloper: {DEV_EN} ({DEV_AR}) — {DEV_URL}\nFull text: {SITE}/llms-full.txt\n\n## English\n\n{li(en_main, "")}\n\n## العربية (Arabic)\n\n{li(ar_index, "ar/")}\n')
wr(OUT + '/llms-full.txt', f'# Nexora Docs — full text\nDeveloper: {DEV_EN} ({DEV_AR}) — {DEV_URL}\n\n' + '\n\n'.join(f'## {i["t"]}\nURL: {SITE}/{i["u"]}\n{i["d"]}\n\n{i["x"]}' for i in en_index) + '\n\n# العربية\n\n' + '\n\n'.join(f'## {i["t"]}\nURL: {SITE}/ar/{i["u"]}\n{i["d"]}\n\n{i["x"]}' for i in ar_index) + '\n')
P = '/' + SITE.split('/', 3)[3] if SITE.count('/') > 2 else ''
wr(OUT + '/404.html', f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 — Page not found | الصفحة غير موجودة - Nexora</title>
<meta name="robots" content="noindex,follow"><meta name="author" content="{DEV_EN} | {DEV_AR}">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
<link rel="stylesheet" href="{P}/assets/style.css">
<style>.nf{{min-height:100vh;display:grid;place-items:center;padding:24px;text-align:center}}.nf h1{{font-size:96px;margin:0;line-height:1;color:var(--acc,#4f46e5)}}.nf .box{{max-width:560px}}.nf p{{color:var(--mut)}}
.nf .btns{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:18px 0}}.nf .btns a{{padding:10px 18px;border:1px solid var(--bd);border-radius:10px;font-weight:600;text-decoration:none}}.nf .ar{{direction:rtl;font-family:"Segoe UI",Tahoma,"Noto Sans Arabic",sans-serif;margin-top:20px}}.nf small{{display:block;margin-top:28px;color:var(--mut)}}</style>
</head>
<body><main class="nf"><div class="box"><h1>404</h1>
<h2>Page not found</h2><p>The page you are looking for does not exist or has been moved.</p>
<div class="ar" lang="ar" dir="rtl"><h2>الصفحة غير موجودة</h2><p>الصفحة التي تبحث عنها غير موجودة أو تم نقلها.</p></div>
<div class="btns"><a href="{P}/index.html">Documentation Home</a><a href="{P}/quickstart.html">Quickstart</a><a href="{P}/ar/index.html" lang="ar">التوثيق بالعربية</a></div>
<small>&copy; 2026 <a href="{DEV_URL}" rel="author noopener">{DEV_EN}</a> · <a href="{DEV_URL}" lang="ar" rel="author noopener">{DEV_AR}</a></small></div></main>
<script>if(/^\\{P}\\/ar\\//.test(location.pathname)||(navigator.language||'').indexOf('ar')===0){{document.title='الصفحة غير موجودة (404) - Nexora'}}</script>
</body></html>''')
rm = rd(OUT + '/README.txt')
wr(OUT + '/README.txt', rm + f'\n\nv2: Arabic (RTL) in /ar, 404.html, sitemap.xml, robots.txt, llms.txt, llms-full.txt, SEO meta + JSON-LD.\nSet SITE in build.py to your real domain, then rebuild (or find/replace {SITE}).\nDeveloper: {DEV_EN} ({DEV_AR}) - {DEV_URL}\n')
shutil.copy('/home/claude/build.py', OUT + '/build.py')

# ---------- verify ----------
minidom.parse(OUT + '/sitemap.xml')
bad = []
for fn in os.listdir(OUT + '/ar'):
    if fn.endswith('.html'):
        for l in re.findall(r'href="([^"#]+)"', rd(f'{OUT}/ar/{fn}')):
            if not l.startswith(('http', 'mailto')) and not os.path.exists(os.path.normpath(f'{OUT}/ar/{l}')): bad.append((fn, l))
print('broken ar links:', bad); print('sitemap urls:', len(rows))
os.makedirs('/mnt/user-data/outputs', exist_ok=True)
z = '/mnt/user-data/outputs/nexora-docs-site-v2.zip'
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for r, _, fs in os.walk(OUT):
        for f in fs: zf.write(os.path.join(r, f), os.path.relpath(os.path.join(r, f), OUT))
print('ok')
