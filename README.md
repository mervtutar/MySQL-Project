# MySQL Project
## Yapay Zeka Uzmanlık Programı-Havelsan Veri Yönetimi Modül Projesi

Bu proje, bir kitabevinin veritabanı yönetimini sağlamak için geliştirilmiştir. Projenin ana hedefleri şunlardır:

Veritabanı Oluşturma ve Yönetme: Proje, belirli bir veritabanı şemasına uygun olarak MySQL veritabanı tablolarını oluşturur ve bu tablolara veri ekler. Ayrıca, veritabanı tablolarını silme işlemlerini de gerçekleştirir.

Sorguları İşleme: Proje, belirlenen gereksinimlere uygun olarak çeşitli sorguları gerçekleştirir. Bu sorgular, kitapların en fazla sayfa sayısına sahip olanını bulma, belirli yazarların birlikte yazdığı kitapların yayınevlerini bulma, belirli yazarın en erken yayımlanan kitaplarını bulma gibi işlemleri içerir.

Performans ve Veri Güncelleme: Proje, veritabanı işlemlerini gerçekleştirirken performansı optimize etmeye çalışır ve veri güncelleme işlemlerini yapar. Örneğin, belirli bir anahtar kelimeye sahip kitapların rating'ini artırma ve yeni kitaplar eklenmesi durumunda toplu ekleme işlemleri gerçekleştirme gibi.

Kullanıcı Arayüzü ve Geri Bildirim: Proje, herhangi bir grafik kullanıcı arayüzü tasarlamaz, ancak sorguların sonuçlarını kullanıcıya uygun bir şekilde gösterir. Ayrıca, kullanıcıya işlemler hakkında geri bildirim sağlar.

Projenin amacı, katılımcılara Python programlama dilini kullanarak veritabanı yönetimi konusunda pratik deneyim kazandırmaktır. Ayrıca, MySQL sunucusuna bağlanma, sorgulama ve DML işlemlerini Python kullanarak uygulama becerilerini geliştirmeyi hedefler.

Veritabanı işlemleri ve sorguları `bookdb.py` dosyasında gerçekleştirilir.Projede gerçekleştirilen sorguların tam listesi şu şekildedir:

#### Sorgu 1: En fazla sayfaya sahip kitabın bilgilerini listeleme

#### Sorgu 2: Verilen iki yazarın birlikte yazdığı kitapları yayımlayan yayınevlerinin bilgilerini listeleme

#### Sorgu 3: Verilen yazarın en erken yayımlanan kitaplarının bilgilerini listeleme

#### Sorgu 4: En az 3 kelime içeren isimlere sahip, en az 3 kitap yayımlamış ve tüm kitaplarının ortalama rating'i 3'ten büyük olan yayınevlerinin bilgilerini listeleme

#### Sorgu 5: Verilen yazarın çalıştığı tüm yayınevlerini listeleyen yazarların bilgilerini listeleme

#### Sorgu 6: Yalnızca kendi kitaplarını yayımlayan yayınevleriyle çalışmış yazarların bilgilerini listeleme

#### Sorgu 7: 'Roman' kategorisinde en az 2 kitap yayımlamış ve kitaplarının ortalama rating'i belirtilen değerden büyük olan yayınevlerinin bilgilerini listeleme

#### Sorgu 8: Mağazadaki bazı kitapların birden fazla kez yayımlanmış olabileceği durumda, en düşük rating'e sahip olanların bilgilerini bulma ve phw1 tablosuna toplu ekleme işlemi

#### Sorgu 9: Verilen anahtar kelimeyi içeren kitapların rating'ini bir artırma ve güncelleme işleminden sonra tüm kitapların rating'lerinin toplamını bulma

#### Sorgu 10: Henüz hiç kitap yayımlamamış yayınevlerini silme işlemi ve silme işleminden sonra yayınevleri tablosundaki kayıt sayısını bulma

Bu sorgular, projenin veritabanı yönetimi ve sorgu işlemlerini içeren temel fonksiyonlarını kapsar. 
