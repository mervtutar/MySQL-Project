import mysql.connector
from ibookdb import IBOOKDB
from queryresult import QueryResult

class BOOKDB(IBOOKDB):

    def __init__(self,user,password,host,database,port):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.connection = None

    def initialize(self):
        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            port=self.port
        )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()


    def createTables(self):
        try:
            cursor = self.connection.cursor()

            # Create author table
            cursor.execute("""
                CREATE TABLE author (
                    author_id INT AUTO_INCREMENT PRIMARY KEY,
                    author_name VARCHAR(60)
                )
            """)

            # Create publisher table
            cursor.execute("""
                CREATE TABLE publisher (
                    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
                    publisher_name VARCHAR(50)
                )
            """)

            # Create book table
            cursor.execute("""
                CREATE TABLE book (
                    isbn CHAR(13) PRIMARY KEY,
                    book_name VARCHAR(120),
                    publisher_id INT,
                    first_publish_year CHAR(4),
                    page_count INT,
                    category VARCHAR(25),
                    rating FLOAT,
                    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
                )
            """)

            # Create author_of table
            cursor.execute("""
                CREATE TABLE author_of (
                    isbn CHAR(13),
                    author_id INT,
                    PRIMARY KEY (isbn, author_id),
                    FOREIGN KEY (isbn) REFERENCES book(isbn),
                    FOREIGN KEY (author_id) REFERENCES author(author_id)
                )
            """)

            # Create phw1 table
            cursor.execute("""
                CREATE TABLE phw1 (
                    isbn CHAR(13) PRIMARY KEY,
                    book_name VARCHAR(120),
                    rating FLOAT
                )
            """)

            self.connection.commit()
            cursor.close()
            return 5  # Toplam oluşturulan tablo sayısı
        except Exception as e:
            print("Error creating tables:", e)
            return 0  # Oluşturulan tablo sayısı sıfır


    def dropTables(self) -> int:
        try:
            cursor = self.connection.cursor()

            # Tüm tabloların adlarını al
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]

            # author_of tablosunu diğer tablolardan önce silelim
            if 'author_of' in tables:
                cursor.execute("DROP TABLE IF EXISTS author_of")
                tables.remove('author_of')

            # Kalan tabloları tek tek sil ve silinen tablo sayısını say
            drop_count = 1
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")  # Eğer tablo zaten varsa sil
                drop_count += 1

            # Değişiklikleri veritabanına uygula
            self.connection.commit()

            return drop_count

        except Exception as e:
            print("Error dropping tables:", e)
            return -1  # Hata durumunda -1 döndür

        finally:
            cursor.close()

    def insertAuthor(self,authors):
        try:
            cursor = self.connection.cursor()
            inserted_rows = 0

            for author in authors:
                cursor.execute("""
                    INSERT INTO author (author_id, author_name)
                    VALUES (%s, %s)
                """, (author.author_id, author.author_name))
                inserted_rows += cursor.rowcount

            self.connection.commit()
            cursor.close()
            return inserted_rows
        except Exception as e:
            print("Error inserting authors:", e)
            return 0
      
    def insertBook(self,books):
        try:
            cursor = self.connection.cursor()
            inserted_rows = 0

            for book in books:
                cursor.execute("""
                    INSERT INTO book (isbn, book_name, publisher_id, first_publish_year, page_count, category, rating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (book.isbn, book.book_name, book.publisher_id, book.first_publish_year, book.page_count, book.category, book.rating))
                inserted_rows += cursor.rowcount

            self.connection.commit()
            cursor.close()
            return inserted_rows
        except Exception as e:
            print("Error inserting books:", e)
            return 0
    def insertPublisher(self,publishers):
        try:
            cursor = self.connection.cursor()
            inserted_rows = 0

            for publisher in publishers:
                cursor.execute("""
                    INSERT INTO publisher (publisher_id, publisher_name)
                    VALUES (%s, %s)
                """, (publisher.publisher_id, publisher.publisher_name))
                inserted_rows += cursor.rowcount

            self.connection.commit()
            cursor.close()
            return inserted_rows
        except Exception as e:
            print("Error inserting publishers:", e)
            return 0
    def insertAuthor_of(self,author_ofs):
        try:
            cursor = self.connection.cursor()
            inserted_rows = 0

            for author_of in author_ofs:
                cursor.execute("""
                    INSERT INTO author_of (isbn, author_id)
                    VALUES (%s, %s)
                """, (author_of.isbn, author_of.author_id))
                inserted_rows += cursor.rowcount

            self.connection.commit()
            cursor.close()
            return inserted_rows
        except Exception as e:
            print("Error inserting author_of:", e)
            return 0
    def functionQ1(self) -> list[QueryResult.ResultQ1]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT book.isbn, book.first_publish_year, book.page_count, publisher.publisher_name
                FROM book
                JOIN publisher ON book.publisher_id = publisher.publisher_id
                WHERE book.page_count = (SELECT MAX(page_count) FROM book)
                ORDER BY book.isbn ASC
            """)
            result = cursor.fetchall()
            cursor.close()

            query_results = []
            for row in result:
                query_results.append(QueryResult.ResultQ1(**row))

            return query_results
        except Exception as e:
            print("Error executing functionQ1:", e)
            return []
        
    
    def functionQ2(self, author_id1: int, author_id2: int) -> list[QueryResult.ResultQ2]:
        try:
            cursor = self.connection.cursor()

            # Verilen iki yazarın birlikte yazdığı kitapları yayımlayan yayınevlerinin publisher id'lerini buluyoruz
            query_publisher_ids = """
                SELECT DISTINCT b.publisher_id
                FROM book b
                INNER JOIN author_of ao ON b.isbn = ao.isbn
                WHERE ao.author_id IN (%s, %s)
            """
            cursor.execute(query_publisher_ids, (author_id1, author_id2))
            publisher_ids = [row[0] for row in cursor.fetchall()]

            # Her bir yayınevi için tüm kitapların sayfa sayısının ortalamasını buluyoruz
            q2_results = []
            for publisher_id in publisher_ids:
                query_avg_page_count = """
                    SELECT AVG(page_count) AS avg_page_count
                    FROM book
                    WHERE publisher_id = %s
                """
                cursor.execute(query_avg_page_count, (publisher_id,))
                avg_page_count = cursor.fetchone()[0]

                q2_results.append(QueryResult.ResultQ2(publisher_id, avg_page_count))

            cursor.close()
            return q2_results
        except Exception as e:
            print("Error executing functionQ2:", e)
            return []


    def functionQ3(self, author_name: str) -> list[QueryResult.ResultQ3]:
        try:
            cursor = self.connection.cursor()

            # Verilen yazarın en erken yayımlanan kitabının bilgilerini sorgula
            query = """
                SELECT b.book_name, b.category, b.first_publish_year
                FROM book b
                INNER JOIN author_of ao ON b.isbn = ao.isbn
                INNER JOIN author a ON ao.author_id = a.author_id
                WHERE a.author_name = %s
                ORDER BY b.book_name, b.category, b.first_publish_year
            """
            cursor.execute(query, (author_name,))
            results = cursor.fetchall()

            # Sonuçları QueryResult.ResultQ3 nesneleri olarak düzenle
            q3_results = []
            for row in results:
                book_name, category, first_publish_year = row
                q3_results.append(QueryResult.ResultQ3(book_name, category, first_publish_year))

            cursor.close()
            return q3_results
        except Exception as e:
            print("Error executing functionQ3:", e)
            return []


    def functionQ4(self) -> list[QueryResult.ResultQ4]:
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT publisher.publisher_id, GROUP_CONCAT(DISTINCT book.category ORDER BY book.category) AS categories
                FROM publisher
                INNER JOIN book ON publisher.publisher_id = book.publisher_id
                GROUP BY publisher.publisher_id
                HAVING COUNT(DISTINCT book.isbn) >= 3 AND AVG(book.rating) > 3
                ORDER BY publisher.publisher_id ASC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            q4_results = []
            for row in results:
                publisher_id, categories = row
                category_list = categories.split(',')
                for category in category_list:
                    q4_results.append(QueryResult.ResultQ4(publisher_id, category.strip()))

            cursor.close()
            return q4_results
        except Exception as e:
            print("Error executing functionQ4:", e)
            return []


    def functionQ5(self, author_id: int) -> list[QueryResult.ResultQ5]:
        try:
            cursor = self.connection.cursor()

            # Verilen author_id'nin kitaplarını bul
            query_books = """
                SELECT isbn
                FROM author_of
                WHERE author_id = %s
            """
            cursor.execute(query_books, (author_id,))
            books = cursor.fetchall()

            if books:
                # Kitapların yayınevlerini bul
                publisher_ids = []
                for book in books:
                    query_publisher_id = """
                        SELECT publisher_id
                        FROM book
                        WHERE isbn = %s
                    """
                    cursor.execute(query_publisher_id, (book[0],))
                    publisher_id = cursor.fetchone()[0]
                    publisher_ids.append(publisher_id)

                # Yayınevlerinin yayınladığı kitaplara katkıda bulunan diğer yazarları bul
                other_authors = []
                for publisher_id in publisher_ids:
                    query_other_authors = """
                        SELECT DISTINCT a.author_id, a.author_name
                        FROM author_of ao
                        JOIN author a ON ao.author_id = a.author_id
                        JOIN book b ON ao.isbn = b.isbn
                        WHERE b.publisher_id = %s
                    """
                    cursor.execute(query_other_authors, (publisher_id,))
                    other_authors.extend(cursor.fetchall())

                # Sonuçları sırala ve QueryResult.ResultQ5 nesneleri olarak dönüştür
                other_authors.sort(key=lambda x: x[0])  # author_id'ye göre sırala
                q5_results = [QueryResult.ResultQ5(author_id=author[0], author_name=author[1]) for author in other_authors]

                cursor.close()
                return q5_results
            else:
                print("Bu yazarın kitapları bulunamadı.")
                return []

        except Exception as e:
            print("Error executing functionQ5:", e)
            return []
        
    def functionQ6(self) -> list[QueryResult.ResultQ6]:
        try:
            cursor = self.connection.cursor()

            # Seçici yazarları bulmak için sorguyu oluştur
            query_selective_authors = """
                SELECT DISTINCT ao.author_id
                FROM author_of ao
                JOIN book b ON ao.isbn = b.isbn
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM author_of ao_inner
                    JOIN book b_inner ON ao_inner.isbn = b_inner.isbn
                    WHERE ao_inner.author_id != ao.author_id AND b_inner.publisher_id = b.publisher_id
                )
            """

            cursor.execute(query_selective_authors)
            selective_author_ids = [row[0] for row in cursor.fetchall()]

            # Seçici yazarların kitaplarını ve author_id, isbn bilgilerini listeleyin
            result_q6_list = []
            for author_id in selective_author_ids:
                query_books_by_author = """
                    SELECT author_id, isbn
                    FROM author_of
                    WHERE author_id = %s
                    ORDER BY author_id ASC, isbn ASC
                """
                cursor.execute(query_books_by_author, (author_id,))
                books = cursor.fetchall()
                for book in books:
                    # Yazarın çalıştığı yayınevi ile başka yazarların çalıştığı yayınevlerini kontrol et
                    query_other_publishers = """
                        SELECT DISTINCT b.publisher_id
                        FROM author_of ao
                        JOIN book b ON ao.isbn = b.isbn
                        WHERE ao.author_id != %s AND b.publisher_id IN (
                            SELECT DISTINCT b_inner.publisher_id
                            FROM author_of ao_inner
                            JOIN book b_inner ON ao_inner.isbn = b_inner.isbn
                            WHERE ao_inner.author_id = %s
                        )
                    """
                    cursor.execute(query_other_publishers, (author_id, author_id))
                    other_publishers = cursor.fetchall()
                    if not other_publishers:
                        result_q6_list.append(QueryResult.ResultQ6(author_id=book[0], isbn=book[1]))

            cursor.close()
            return result_q6_list

        except Exception as e:
            print("Error executing functionQ6:", e)
            return []




    def functionQ7(self, rating: float) -> list[QueryResult.ResultQ7]:
        try:
            cursor = self.connection.cursor()

            # SQL sorgusunu hazırla
            query = """
                SELECT p.publisher_id, p.publisher_name
                FROM publisher p
                JOIN book b ON p.publisher_id = b.publisher_id
                WHERE b.category = 'Roman'
                GROUP BY p.publisher_id, p.publisher_name
                HAVING COUNT(DISTINCT b.isbn) >= 2 AND AVG(b.rating) > %s
                ORDER BY p.publisher_id ASC
            """

            # Sorguyu çalıştır ve sonuçları al
            cursor.execute(query, (rating,))
            results = cursor.fetchall()

            # Sonuçları ResultQ7 nesneleri olarak dönüştür
            q7_results = [QueryResult.ResultQ7(publisher_id=result[0], publisher_name=result[1]) for result in results]

            cursor.close()
            return q7_results

        except Exception as e:
            print("Error executing functionQ7:", e)
            return []


    
    def functionQ8(self) -> list[QueryResult.ResultQ8]:
        results = []

        try:
            cursor = self.connection.cursor()

            # Aynı isme sahip kitapları bul
            query_same_name_books = """
                SELECT book_name
                FROM book
                GROUP BY book_name
                HAVING COUNT(*) > 1
            """
            cursor.execute(query_same_name_books)
            same_name_books = [row[0] for row in cursor.fetchall()]

            for book_name in same_name_books:
                # Her bir kitap adı için en düşük puana sahip olanların ISBN, kitap adı ve puanlarını bul
                query_lowest_rating_books = """
                    SELECT isbn, book_name, rating
                    FROM book
                    WHERE book_name = %s
                    ORDER BY rating ASC
                    LIMIT 1
                """
                cursor.execute(query_lowest_rating_books, (book_name,))
                lowest_rating_books = cursor.fetchall()

                # Bulunan verileri phw1 tablosuna ekleyin
                insert_query = """
                    INSERT INTO phw1 (isbn, book_name, rating) VALUES (%s, %s, %s)
                """
                cursor.executemany(insert_query, lowest_rating_books)

                # En düşük puanlı kitapları sonuç listesine ekle
                for row in lowest_rating_books:
                    isbn, book_name, rating = row
                    results.append(QueryResult.ResultQ8(isbn=isbn, book_name=book_name, rating=rating))

            # Veritabanı üzerinde yapılan değişiklikleri onayla
            self.connection.commit()

        except Exception as e:
            print("Error executing functionQ8:", e)

        finally:
            cursor.close()

        return results

        
    def functionQ9(self, keyword: str) -> float:
        try:
            cursor = self.connection.cursor()

            # Anahtar kelimeyi içeren ve içermeyen kitapları bul
            query_books_with_keyword = """
                SELECT isbn, book_name, rating
                FROM book
                WHERE book_name LIKE %s
            """
            cursor.execute(query_books_with_keyword, ('%' + keyword + '%',))
            books_with_keyword = cursor.fetchall()

            total_rating = 0  # Toplam rating'i saklamak için bir değişken

            # Her bir kitap için rating'i kontrol et ve toplam rating'e ekle
            for book in books_with_keyword:
                isbn, book_name, rating = book
                if rating <= 4:  # Rating 4'ten küçükse ve 1 artırıldığında 5'ten küçük olacaksa
                    new_rating = min(rating + 1, 5)  # Yeni rating'i hesapla, maksimum 5 olacak şekilde
                    total_rating += new_rating  # Toplam rating'e ekle

                    # Rating'i güncelle
                    update_query = """
                        UPDATE book
                        SET rating = %s
                        WHERE isbn = %s
                    """
                    cursor.execute(update_query, (new_rating, isbn))

                else:
                    # Rating 4'ten büyükse, kitabın rating'ini güncelleme
                    total_rating += rating  # Toplam rating'e mevcut rating'i ekle

            # Anahtar kelimeye sahip olmayan kitapları bul
            query_books_without_keyword = """
                SELECT rating
                FROM book
                WHERE book_name NOT LIKE %s
            """
            cursor.execute(query_books_without_keyword, ('%' + keyword + '%',))
            books_without_keyword = cursor.fetchall()

            # Anahtar kelimeye sahip olmayan kitapların rating'lerini toplam rating'e ekle
            for rating in books_without_keyword:
                total_rating += rating[0]

            # Veritabanı üzerinde yapılan değişiklikleri onayla
            self.connection.commit()

            # Tüm kitapların rating'lerinin toplamını döndür
            return total_rating

        except Exception as e:
            print("Error executing functionQ9:", e)
            return -1  # Hata durumunda -1 döndür

        finally:
            cursor.close()



    def function10(self) -> int:
        try:
            cursor = self.connection.cursor()

            # Henüz hiç kitap yayımlamamış yayınevlerini bul
            query_delete_publishers = """
                DELETE FROM publisher
                WHERE publisher_id NOT IN (
                    SELECT DISTINCT publisher_id
                    FROM book
                )
            """

            # Silme işlemini gerçekleştir
            cursor.execute(query_delete_publishers)

            # Veritabanı üzerinde yapılan değişiklikleri onayla
            self.connection.commit()

            # Silme işleminden sonra kalan kayıt sayısını al
            query_remaining_publishers = """
                SELECT COUNT(*) FROM publisher
            """
            cursor.execute(query_remaining_publishers)
            remaining_count = cursor.fetchone()[0]

            return remaining_count

        except Exception as e:
            print("Error executing function10:", e)
            return -1  # Hata durumunda -1 döndür

        finally:
            cursor.close()

