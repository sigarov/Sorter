"""Türkçe kılavuz — Almanca özgün metin manual/de.py'nin çevirisi."""

TR = {
    "title": "Kullanım Kılavuzu",
    "sections": [
        {
            "id": "intro",
            "title": "1. Program ne yapar",
            "text": (
                "Medya Sıralayıcı, resimleri ve videoları sabit bir klasör yapısına yerleştirir "
                "ve ardından yinelenen adların temizlenmesine yardımcı olur.\n\n"
                "Bir veya iki kaynak (klasörler ya da tüm sürücüler) ve bir hedef klasör "
                "seçersin. Program tüm resimleri ve videoları okur, çekim tarihini belirler ve "
                "her dosyayı uygun yıl, ay ve gün klasörüne kopyalar.\n\n"
                "Bilinmesi gerekenler:\n"
                "• Kaynaklar yalnızca okunur, asla değiştirilmez.\n"
                '• Hiçbir şey silinmez. Yinelenenler "Duplicates" klasörüne gider.\n'
                "• Hedefteki klasör adları her zaman İngilizcedir (Pictures, Videos, "
                "_No_Date). Böylece dil değiştiğinde yapı sabit kalır.\n"
                "• Arayüz yedi dilde sunulur. Bu kılavuz, çevirisi olduğunda seçilen dilde "
                "görünür; o zamana kadar Almanca görünür."
            ),
        },
        {
            "id": "start",
            "title": "2. İlk adımlar",
            "text": (
                "1. Sol üstten dili seç — görünüm hemen değişir.\n"
                "2. Kaynak 1'i seç: klasör veya sürücü. İstersen kaynak 2'yi ekle.\n"
                "3. Hedefi seç: sıralama oraya yapılır.\n"
                "4. İstersen önce simülasyon için deneme çalıştırmasını etkinleştir.\n"
                '5. "▶  Başlat" düğmesine tıkla (veya F5\'e bas).\n\n'
                "Çalışma sırasında iki ilerleme çubuğu durumu gösterir: önce hedefin "
                'dizinlenmesi, sonra sıralama. "■  Durdur" (veya Esc) ile iptal edersin; '
                "zaten kopyalanmış dosyalar korunur.\n\n"
                '"Temizle" sekmesi, seçilen hedefte gerçek bir sıralama çalıştırması '
                "yapıldıktan sonra açılır."
            ),
        },
        {
            "id": "sort",
            "title": "3. Sıralama ve klasör yapısı",
            "text": (
                "Sıralama iki aşamadan oluşur:\n"
                "1. Hedef klasör dizinlenir. Mevcut tüm dosyaların boyutu, değişiklik zamanı "
                "ve sağlama toplamı (hash) kaydedilir.\n"
                "2. Her kaynak dosya denetlenir ve hedef klasöre kopyalanır.\n\n"
                "Tarih şu sırayla belirlenir:\n"
                "• Resmin EXIF çekim tarihi (Pillow gerekir)\n"
                "• Video meta verileri (PATH'te ffprobe gerekir)\n"
                "• Dosya adından tarih, ör. 2020-05-17, 20200517 veya 20200517_143025\n\n"
                "Dosya sistemi tarihi bilinçli olarak kullanılmaz: gerçek zaman damgası "
                "olmayan dosyalar, kopyalama tarihine göre yanlış sıralanmak yerine _No_Date "
                "klasörüne gitmelidir.\n\n"
                "Hedefteki yapı (örnek):\n"
                "• Pictures/2020/05/17/tatil.jpg\n"
                "• Videos/2020/05/17/tatil.mp4\n"
                "• _No_Date/Pictures/bilinmeyen.jpg\n\n"
                "Hedef dosya zaten varsa ve içerik aynıysa kaynak dosya atlanır. Ad aynı ama "
                "içerik farklıysa _1, _2 vb. oluşur. Program kopyalamadan önce boş disk alanını "
                "denetler, kopyaladıktan sonra dosya boyutunu karşılaştırır."
            ),
        },
        {
            "id": "names",
            "title": "4. Dosya adları",
            "text": (
                "Yeni dosya adları için altı varyant (örnek: 17.05.2020, 14:30:25 tarihli "
                "tatil.jpg):\n\n"
                "• Orijinal: tatil.jpg\n"
                "• Tarih_Ad: 20200517_tatil.jpg\n"
                "• Tarih_Saat_Ad: 20200517_143025_tatil.jpg\n"
                "• Yıl-Ay-Gün_Ad: 2020-05-17_tatil.jpg\n"
                "• Numara: 00001.jpg\n"
                "• Tarih_Numara: 20200517_0001.jpg\n\n"
                'Tarih yoksa "Numara" yalnızca sıra numarasını verir; diğer tüm varyantlarda '
                "özgün ad korunur. Uzantı her zaman küçük harfle yazılır. Adlar çakışırsa "
                "program _1, _2, ... ekler."
            ),
        },
        {
            "id": "structure",
            "title": "5. Yapı: ayrı veya birlikte",
            "text": (
                "Ayrı (varsayılan): resimler ve videolar kendi ağaçlarında bulunur.\n"
                "  Pictures/2020/05/17/... ve Videos/2020/05/17/...\n"
                "Birlikte: ikisi de aynı yıl/ay/gün klasörüne gider.\n"
                "  2020/05/17/...\n\n"
                "Ayrıntı düzeyi:\n"
                "• Yıl: 2020/\n"
                "• Ay: 2020/05/\n"
                "• Gün: 2020/05/17/\n\n"
                'Tarihi olmayan dosyalar _No_Date klasörüne gider; "Ayrı" seçeneğinde ayrıca '
                "Pictures veya Videos altına. Orada _liste.txt tüm ilgili dosyaları listeler."
            ),
        },
        {
            "id": "filters",
            "title": "6. Klasörleri filtreleme",
            "text": (
                "Filtre alanı, kaynağın hangi alt klasörlerinin taranacağını sınırlar.\n"
                "• Birden çok terimi virgülle ayır: Fotoğraflar, Pictures, DCIM\n"
                "• Yalnızca klasör adları dikkate alınır, dosya uzantıları değil.\n"
                "• Büyük/küçük harf fark etmez.\n"
                "• Bir eşleşme tüm alt klasörler için de geçerlidir.\n"
                "• Boş alan = kaynağın tamamı.\n\n"
                'Örnek: D:\\Backup içinde "Fotoğraflar", "Belgeler" ve "Videolar" var. '
                '"Fotoğraflar, Videolar" filtresiyle yalnızca bu iki klasör okunur.\n\n'
                '"Temizle" sekmesinde filtre yoktur: orada her zaman hedef klasörün tamamı '
                "denetlenir."
            ),
        },
        {
            "id": "dryrun",
            "title": "7. Deneme çalıştırması ve dizin önbelleği",
            "text": (
                "Deneme çalıştırması, hiçbir şeyi değiştirmeden ne olacağını gösterir:\n"
                "• Hiçbir şey kopyalanmaz, taşınmaz veya yeniden adlandırılmaz.\n"
                '• _index.txt oluşmaz, bu nedenle deneme çalıştırması "Temizle" sekmesini '
                "açmaz.\n"
                "• Planlanan işlemler günlükte ve _log_dry.txt içinde görünür.\n\n"
                "Buna rağmen deneme çalıştırması hedef klasörü okur ve uygulama klasöründe bir "
                "hash önbelleği kaydeder. Sonraki gerçek çalıştırma bu önbelleği kullanır ve "
                "ardından siler. Bu, ikinci geçişte çok zaman kazandırır."
            ),
        },
        {
            "id": "dedup",
            "title": "8. Yinelenenleri temizleme",
            "text": (
                '"Temizle" sekmesi, sıralama sırasında oluşan yinelenen adları temizler. '
                "Yalnızca hedef klasörde çalışır ve ancak orada gerçek bir sıralama "
                "çalıştırması yapıldıysa açılır (_index.txt dosyasından anlaşılır).\n\n"
                "Gruplar: NAME.jpg, NAME_1.jpg, NAME_2.jpg ... birbirine aittir.\n\n"
                "Standart kural:\n"
                "• Bir _1, _2 dosyası temel dosyayla bayt bayt aynıysa Duplicates klasörüne "
                "taşınır. Temel dosya hedef klasörde kalır.\n"
                "• Temel dosya, iki sürümü doğrudan karşılaştırabilmen için grup başına bir kez "
                "Duplicates klasörüne kopyalanır.\n"
                "• İçerik farklıysa dosyaya dokunulmaz.\n\n"
                "Genişletilmiş kural (Force):\n"
                "• İçeriği farklı olan _1, _2 dosyaları da içerik karşılaştırılmadan Duplicates "
                "klasörüne taşınır. Program önce onay ister.\n"
                "• Aynı ada sahip yedekler ve dosya adları rastlantıyla aynı olan iki kamera "
                "için düşünülmüştür.\n\n"
                "Temel dosya yoksa en küçük numaralı dosya temel ada dönüştürülür "
                "(IMG_1.jpg -> IMG.jpg). Dosya hedef klasörde kalır.\n\n"
                "Hiçbir şey silinmez: Duplicates klasör yapısını yansıtır ve sonraki sıralamada "
                "atlanır. Temizliği kendin yaparsın. Deneme çalıştırması burada da çalışır ve "
                "yalnızca deneme günlüğüne yazar."
            ),
        },
        {
            "id": "skip",
            "title": "9. Mevcut dosyaları atlama",
            "text": (
                '"Mevcut dosyaları atla", _1, _2 dosyalarının oluşmasını önler: hedef dosya '
                "zaten varsa değişmeden kalır ve kaynak dosya atlanır.\n\n"
                "Bu seçenek, farklı zaman damgalarıyla kaydedilmiş yedekler için düşünülmüştür: "
                "_1 dosyası olarak ikinci bir sürüm oluşturmak yerine ilki korunur. Günlükte bu "
                "dosyalar SKIP (mevcut) olarak görünür ve yinelenen sayılır.\n\n"
                "Bu seçenek olmadan aynı ada sahip dosyalar _1, _2 dosyalarına dönüşür; bunları "
                'daha sonra "Temizle" sekmesinde denetleyebilirsin.'
            ),
        },
        {
            "id": "log",
            "title": "10. Günlük penceresi",
            "text": (
                "Günlük, çalıştırmanın tüm işlemlerini renkli olarak gösterir:\n"
                "• mavi: bilgiler\n"
                "• sarı: uyarılar\n"
                "• kırmızı: hatalar\n"
                "• yeşil: rapor/özet\n\n"
                "Kullanım:\n"
                '• "Sadece hatalar": diğer her şeyi gizler.\n'
                '• "Otomatik kaydır": otomatik olarak sona gider.\n'
                "• Arama alanı + Enter: bir sonraki eşleşmeye gider (büyük/küçük harf fark "
                "etmez).\n"
                '• "Temizle" (Ctrl+L), "Kaydet" (Ctrl+S), "Aç".\n\n'
                "Günlük, uzun çalıştırmaların belleği doldurmaması için 50.000 satırla "
                "sınırlıdır. Hedef klasörde ayrıca _log.txt bulunur; deneme çalıştırmasında "
                "onun yerine _log_dry.txt."
            ),
        },
        {
            "id": "settings",
            "title": "11. Ayarlar, konum ve dil",
            "text": (
                "Veriler kullanıcı dizininde ~/.medien_sortierer altında saklanır:\n"
                "• settings.json: pencere boyutu, dil ve son seçilen klasörler\n"
                "• app.log: teknik program günlüğü\n\n"
                "Ayarlar kapanışta yazılır ve bir sonraki başlatmada yeniden yüklenir. Dil "
                "yeniden başlatma olmadan hemen etkili olur.\n\n"
                "Gerçek bir çalıştırmadan sonra hedef klasör şunları içerir:\n"
                '• _index.txt: sonraki çalıştırmaları hızlandıran dosya dizini ve "burada '
                'zaten sıralandı" işareti ("Temizle" sekmesini açar)\n'
                "• _log.txt: çalıştırmanın günlüğü\n"
                "• Duplicates: ayrılan yinelenen adlar\n\n"
                "Kaynak hedefle aynıysa program otomatik olarak Sorted alt klasörüne sıralar. "
                "Hedef klasörün kendisi hiçbir zaman kaynak olarak taranmaz."
            ),
        },
        {
            "id": "keys",
            "title": "12. Klavye kısayolları ve sorun giderme",
            "text": (
                "Klavye kısayolları:\n"
                "• F1 — bu kılavuzu aç\n"
                "• F5 — çalıştırmayı başlat\n"
                "• Esc — çalıştırmayı durdur\n"
                "• Ctrl+L — günlüğü temizle\n"
                "• Ctrl+S — günlüğü kaydet\n\n"
                "Grupların yanındaki küçük ? düğmeleri ilgili alan için kısa ipuçları gösterir.\n\n"
                "Bir şey beklenildiği gibi çalışmazsa:\n"
                "• Her şey _No_Date klasörüne gidiyor: tarih bulunamadı. EXIF verileri için "
                "Pillow kur, videolar için ffprobe sağla.\n"
                '• "Temizle" sekmesi kilitli: bu hedefte henüz gerçek bir sıralama '
                "çalıştırması olmadı. Önce sırala — deneme çalıştırması yeterli değildir.\n"
                '• Dosyalar _1, _2 olarak adlandırılıyor: ad çakışması oldu. "Temizle" '
                "sekmesinde düzenle.\n"
                "• Sıralamadan sonra dosyalar eksik: aynı içerikle zaten vardılar ve yinelenen "
                "olarak atlandılar — günlük onları DUP olarak gösterir.\n"
                '• Çalıştırma "Yeterli disk alanı yok" ile kesiliyor: hedefte yer aç veya '
                "başka bir hedef sürücü seç."
            ),
        },
    ],
}
