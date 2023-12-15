import unittest
import refservice
from util import ResultState
from test_util import init_test, MockupRequest

init_sql = """
INSERT INTO users (id, username, password) VALUES (1, 'test_user', 'test_password');
INSERT INTO inproceedings (cite_id, author, title, year, booktitle, start_page, end_page, user_id)  VALUES ('test_id_1', 'test_1_author', 'test_1_title', 1, 'test_1_booktitle', 1, 2, 1);
INSERT INTO inproceedings (cite_id, author, title, year, booktitle, start_page, end_page, user_id)  VALUES ('test_id_2', 'test_2_author', 'test_2_title', 1, 'test_2_booktitle', 1, 2, 1);
INSERT INTO articles (cite_id, author, title, journal, year, volume, start_page, end_page, user_id)  VALUES ('test_id_3', 'test_3_author', 'test_3_title', 'test_3_journal', 1, 2, 1, 2, 1);
INSERT INTO articles (cite_id, author, title, journal, year, volume, start_page, end_page, user_id)  VALUES ('test_id_4', 'test_4_author', 'test_4_title', 'test_4_journal', 1, 2, 1, 2, 1);
INSERT INTO books (cite_id, author, title, year, publisher, start_page, end_page, user_id)  VALUES ('test_id_5', 'test_5_author', 'test_5_title', 1, 'test_5_publisher', 1, 2, 1);
INSERT INTO books (cite_id, author, title, year, publisher, start_page, end_page, user_id)  VALUES ('test_id_6', 'test_6_author', 'test_6_title', 1, 'test_6_publisher', 1, 2, 1);
INSERT INTO tags (name, user_id) VALUES ('test tag 1', 1);
INSERT INTO tags (name, user_id) VALUES ('test tag 2', 1);
"""

class RefServiceTest(unittest.TestCase):
	def setUp(self):
		self.app, self.db = init_test(init_sql)

	def test_add_book_to_database(self):
		with self.app.app_context():
			initial_books = refservice.list_books(self.db, 1)

			request = MockupRequest({
				"cite_id":   "some_cite_id",
				"title":     "Some Title",
				"author":    "Some Author",
				"year":       2001,
				"publisher": "Some Publisher",
				"start_page": 101,
				"end_page":   256,
				"user_id":    1
			})

			res = refservice.add_book_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_books = refservice.list_books(self.db, 1)
			added_books = set(curr_books) - set(initial_books)

			self.assertEqual(len(added_books), 1)
			added_book = added_books.pop()

			self.assertEqual(added_book.cite_id,   "some_cite_id")
			self.assertEqual(added_book.title,     "Some Title")
			self.assertEqual(added_book.author,    "Some Author")
			self.assertEqual(added_book.year,       2001)
			self.assertEqual(added_book.publisher, "Some Publisher")
			self.assertEqual(added_book.start_page, 101)
			self.assertEqual(added_book.end_page,   256)
			self.assertEqual(added_book.user_id,    1)

	def test_add_article_to_database(self):
		with self.app.app_context():
			initial_articles = refservice.list_articles(self.db, 1)

			request = MockupRequest({
				"cite_id":   "some_cite_id",
				"author":    "Some Author",
				"title":     "Some Title",
				"journal":   "Some Journal",
				"year":       2002,
				"volume":     3,
				"start_page": 202,
				"end_page":   500,
				"user_id":    1
			})

			res = refservice.add_article_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_articles = refservice.list_articles(self.db, 1)
			added_articles = set(curr_articles) - set(initial_articles)

			self.assertEqual(len(added_articles), 1)
			added_article = added_articles.pop()

			self.assertEqual(added_article.cite_id,   "some_cite_id")
			self.assertEqual(added_article.author,    "Some Author")
			self.assertEqual(added_article.title,     "Some Title")
			self.assertEqual(added_article.journal,   "Some Journal")
			self.assertEqual(added_article.year,       2002)
			self.assertEqual(added_article.volume,     3)
			self.assertEqual(added_article.start_page, 202)
			self.assertEqual(added_article.end_page,   500)
			self.assertEqual(added_article.user_id,    1)

	def test_add_inproceeding_to_database(self):
		with self.app.app_context():
			initial_inproceedings = refservice.list_inproceedings(self.db, 1)

			request = MockupRequest({
				"cite_id":   "some_cite_id",
				"title":     "Some Title",
				"author":    "Some Author",
				"year":       2003,
				"booktitle": "Some Book Title",
				"start_page": 303,
				"end_page":   444,
				"user_id":    1
			})

			res = refservice.add_inproceeding_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_inproceedings = refservice.list_inproceedings(self.db, 1)
			added_inproceedings = set(curr_inproceedings) - set(initial_inproceedings)

			self.assertEqual(len(added_inproceedings), 1)
			added_inproceeding = added_inproceedings.pop()

			self.assertEqual(added_inproceeding.cite_id,   "some_cite_id")
			self.assertEqual(added_inproceeding.title,     "Some Title")
			self.assertEqual(added_inproceeding.author,    "Some Author")
			self.assertEqual(added_inproceeding.year,       2003)
			self.assertEqual(added_inproceeding.booktitle, "Some Book Title")
			self.assertEqual(added_inproceeding.start_page, 303)
			self.assertEqual(added_inproceeding.end_page,   444)
			self.assertEqual(added_inproceeding.user_id,    1)

	def test_add_book_with_missing_fields(self):
		with self.app.app_context():
			initial_books = refservice.list_books(self.db, 1)

			request = MockupRequest({
				"cite_id":    "some_cite_id",
				"title":      "Some Title",
				"author":     "",
				"year":       "",
				"publisher":  "",
				"start_page": "",
				"end_page":   "",
				"user_id":    1
			})

			res = refservice.add_book_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_books = refservice.list_books(self.db, 1)
			added_books = set(curr_books) - set(initial_books)

			self.assertEqual(len(added_books), 1)
			added_book = added_books.pop()

			self.assertEqual(added_book.cite_id,    "some_cite_id")
			self.assertEqual(added_book.title,      "Some Title")
			self.assertEqual(added_book.author,     "")
			self.assertEqual(added_book.year,       None)
			self.assertEqual(added_book.publisher,  "")
			self.assertEqual(added_book.start_page, None)
			self.assertEqual(added_book.end_page,   None)
			self.assertEqual(added_book.user_id,    1)

	def test_add_article_with_missing_fields(self):
		with self.app.app_context():
			initial_articles = refservice.list_articles(self.db, 1)

			request = MockupRequest({
				"cite_id":    "some_cite_id",
				"title":      "Some Title",
				"author":     "",
				"journal":    "",
				"year":       "",
				"volume":     "",
				"start_page": "",
				"end_page":   "",
				"user_id":    1
			})

			res = refservice.add_article_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_articles = refservice.list_articles(self.db, 1)
			added_articles = set(curr_articles) - set(initial_articles)

			self.assertEqual(len(added_articles), 1)
			added_article = added_articles.pop()

			self.assertEqual(added_article.cite_id,    "some_cite_id")
			self.assertEqual(added_article.title,      "Some Title")
			self.assertEqual(added_article.author,     "")
			self.assertEqual(added_article.journal,    "")
			self.assertEqual(added_article.year,       None)
			self.assertEqual(added_article.volume,     None)
			self.assertEqual(added_article.start_page, None)
			self.assertEqual(added_article.end_page,   None)
			self.assertEqual(added_article.user_id,    1)

	def test_add_inproceeding_with_missing_fields(self):
		with self.app.app_context():
			initial_inproceedings = refservice.list_inproceedings(self.db, 1)

			request = MockupRequest({
				"cite_id":    "some_cite_id",
				"title":      "Some Title",
				"author":     "",
				"year":       "",
				"booktitle":  "",
				"start_page": "",
				"end_page":   "",
				"user_id":    1
			})

			res = refservice.add_inproceeding_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_inproceedings = refservice.list_inproceedings(self.db, 1)
			added_inproceedings = set(curr_inproceedings) - set(initial_inproceedings)

			self.assertEqual(len(added_inproceedings), 1)
			added_inproceeding = added_inproceedings.pop()

			self.assertEqual(added_inproceeding.cite_id,    "some_cite_id")
			self.assertEqual(added_inproceeding.title,      "Some Title")
			self.assertEqual(added_inproceeding.author,     "")
			self.assertEqual(added_inproceeding.year,       None)
			self.assertEqual(added_inproceeding.booktitle,  "")
			self.assertEqual(added_inproceeding.start_page, None)
			self.assertEqual(added_inproceeding.end_page,   None)
			self.assertEqual(added_inproceeding.user_id,    1)

	def test_add_duplicate(self):
		with self.app.app_context():
			num_initial_books = len(refservice.list_books(self.db, 1))

			request = MockupRequest({
				"cite_id":   "some_cite_id",
				"title":     "Some Title",
				"author":    "Some Author",
				"year":       2001,
				"publisher": "Some Publisher",
				"start_page": 101,
				"end_page":   256,
				"user_id":    1
			})

			res = refservice.add_book_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			num_curr_books = len(refservice.list_books(self.db, 1))
			self.assertEqual(num_curr_books, num_initial_books + 1)

			res = refservice.add_book_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.duplicate_cite_id)

			num_curr_books = len(refservice.list_books(self.db, 1))
			self.assertEqual(num_curr_books, num_initial_books + 1)

	def test_add_book_from_doi(self):
		with self.app.app_context():
			initial_books = refservice.list_books(self.db, 1)

			request = MockupRequest({
				"doi": "10.1007/3-540-49126-0",
				"cite_id":   "some_cite_id",
				"start_page": 100,
				"end_page":   200,
				"user_id":    1
			})

			res = refservice.add_from_doi(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_books = refservice.list_books(self.db, 1)
			added_books = set(curr_books) - set(initial_books)

			self.assertEqual(len(added_books), 1)
			added_book = added_books.pop()

			self.assertEqual(added_book.cite_id,   "some_cite_id")
			self.assertEqual(added_book.title,     "Discrete Geometry for Computer Imagery")
			self.assertEqual(added_book.author,     None)
			self.assertEqual(added_book.year,       1999)
			self.assertEqual(added_book.publisher, "Springer Berlin Heidelberg")
			self.assertEqual(added_book.start_page, 100)
			self.assertEqual(added_book.end_page,   200)
			self.assertEqual(added_book.user_id,    1)

	def test_add_article_from_doi(self):
		with self.app.app_context():
			initial_articles = refservice.list_articles(self.db, 1)

			request = MockupRequest({
				"doi": "10.1145/159544.159617",
				"cite_id":   "some_cite_id",
				"user_id":    1
			})

			res = refservice.add_from_doi(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_articles = refservice.list_articles(self.db, 1)
			added_articles = set(curr_articles) - set(initial_articles)

			self.assertEqual(len(added_articles), 1)
			added_article = added_articles.pop()

			self.assertEqual(added_article.cite_id,   "some_cite_id")
			self.assertEqual(added_article.author,    "Weiser, Mark")
			self.assertEqual(added_article.title,     "Some computer science issues in ubiquitous computing")
			self.assertEqual(added_article.journal,   "Communications of the ACM")
			self.assertEqual(added_article.year,       1993)
			self.assertEqual(added_article.volume,     36)
			self.assertEqual(added_article.start_page, 75)
			self.assertEqual(added_article.end_page,   84)
			self.assertEqual(added_article.user_id,    1)

	def test_add_from_invalid_doi(self):
		with self.app.app_context():
			num_initial_books = len(refservice.list_books(self.db, 1))

			request = MockupRequest({
				"doi":       "obviously invalid",
				"cite_id":   "some_cite_id",
				"user_id":    1
			})

			res = refservice.add_from_doi(self.db, request, 1)
			self.assertEqual(res, ResultState.doi_not_found)

			num_curr_books = len(refservice.list_books(self.db, 1))
			self.assertEqual(num_curr_books, num_initial_books)

	def test_add_duplicate_from_doi(self):
		with self.app.app_context():
			num_initial_books = len(refservice.list_books(self.db, 1))

			request = MockupRequest({
				"doi": "10.1007/3-540-49126-0",
				"cite_id":   "some_cite_id",
				"start_page": 100,
				"end_page":   200,
				"user_id":    1
			})

			res = refservice.add_from_doi(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			num_curr_books = len(refservice.list_books(self.db, 1))
			self.assertEqual(num_curr_books, num_initial_books + 1)

			res = refservice.add_from_doi(self.db, request, 1)
			self.assertEqual(res, ResultState.duplicate_cite_id)

			num_curr_books = len(refservice.list_books(self.db, 1))
			self.assertEqual(num_curr_books, num_initial_books + 1)

	def test_list_book_references(self):
		with self.app.app_context():
			books = refservice.list_references(self.db, 1)[0]
			self.assertEqual(len(books), 2)

			self.assertEqual(books[0].cite_id, 'test_id_5')
			self.assertEqual(books[0].author, 'test_5_author')
			self.assertEqual(books[0].title, 'test_5_title')
			self.assertEqual(books[0].year, 1)
			self.assertEqual(books[0].publisher, 'test_5_publisher')
			self.assertEqual(books[0].start_page, 1)
			self.assertEqual(books[0].end_page, 2)
			self.assertEqual(books[0].user_id, 1)

			self.assertEqual(books[1].cite_id, 'test_id_6')
			self.assertEqual(books[1].author, 'test_6_author')
			self.assertEqual(books[1].title, 'test_6_title')
			self.assertEqual(books[1].year, 1)
			self.assertEqual(books[1].publisher, 'test_6_publisher')
			self.assertEqual(books[1].start_page, 1)
			self.assertEqual(books[1].end_page, 2)
			self.assertEqual(books[1].user_id, 1)

	def test_list_article_references(self):
		with self.app.app_context():
			articles = refservice.list_references(self.db, 1)[1]
			self.assertEqual(len(articles), 2)

			self.assertEqual(articles[0].cite_id, 'test_id_3')
			self.assertEqual(articles[0].author, 'test_3_author')
			self.assertEqual(articles[0].title, 'test_3_title')
			self.assertEqual(articles[0].journal, 'test_3_journal')
			self.assertEqual(articles[0].year, 1)
			self.assertEqual(articles[0].volume, 2)
			self.assertEqual(articles[0].start_page, 1)
			self.assertEqual(articles[0].end_page, 2)
			self.assertEqual(articles[0].user_id, 1)

			self.assertEqual(articles[1].cite_id, 'test_id_4')
			self.assertEqual(articles[1].author, 'test_4_author')
			self.assertEqual(articles[1].title, 'test_4_title')
			self.assertEqual(articles[1].journal, 'test_4_journal')
			self.assertEqual(articles[1].year, 1)
			self.assertEqual(articles[1].volume, 2)
			self.assertEqual(articles[1].start_page, 1)
			self.assertEqual(articles[1].end_page, 2)
			self.assertEqual(articles[1].user_id, 1)

	def test_list_inproceeding_references(self):
		with self.app.app_context():
			inproceedings = refservice.list_references(self.db, 1)[2]
			self.assertEqual(len(inproceedings), 2)

			self.assertEqual(inproceedings[0].cite_id, 'test_id_1')
			self.assertEqual(inproceedings[0].author, 'test_1_author')
			self.assertEqual(inproceedings[0].title, 'test_1_title')
			self.assertEqual(inproceedings[0].year, 1)
			self.assertEqual(inproceedings[0].booktitle, 'test_1_booktitle')
			self.assertEqual(inproceedings[0].start_page, 1)
			self.assertEqual(inproceedings[0].end_page, 2)
			self.assertEqual(inproceedings[0].user_id, 1)

			self.assertEqual(inproceedings[1].cite_id, 'test_id_2')
			self.assertEqual(inproceedings[1].author, 'test_2_author')
			self.assertEqual(inproceedings[1].title, 'test_2_title')
			self.assertEqual(inproceedings[1].year, 1)
			self.assertEqual(inproceedings[1].booktitle, 'test_2_booktitle')
			self.assertEqual(inproceedings[1].start_page, 1)
			self.assertEqual(inproceedings[1].end_page, 2)
			self.assertEqual(inproceedings[1].user_id, 1)

	def test_list_references_no_user(self):
		with self.app.app_context():
			books, articles, inproceedings = refservice.list_references(self.db, None)

			self.assertEqual(len(books), 0)
			self.assertEqual(len(articles), 0)
			self.assertEqual(len(inproceedings), 0)

	def test_add_new_tag(self):
		with self.app.app_context():
			initial_tags = refservice.get_tags_for_user(self.db, 1)

			request = MockupRequest({"name": "new test tag"})
			refservice.add_new_tag(self.db, request, 1)

			curr_tags = refservice.get_tags_for_user(self.db, 1)
			added_tags = set(curr_tags) - set(initial_tags)

			self.assertEqual(len(added_tags), 1)
			added_tag = added_tags.pop()

			self.assertEqual(added_tag.name, "new test tag")

			for initial_tag in initial_tags:
				self.assertNotEqual(added_tag.id, initial_tag.id)

	def test_add_tag_to_reference(self):
		with self.app.app_context():
			initial_books = refservice.list_books(self.db, 1)

			request = MockupRequest({
				"cite_id": "some_cite_id",
				"author": "Some Author",
				"title": "Some Title",
				"year": 1,
				"publisher": "Some Publisher",
				"start_page": 1,
				"end_page": 2,
				"user_id": 1,
				'1': 'on'
			})

			res = refservice.add_book_to_database(self.db, request, 1)
			self.assertEqual(res, ResultState.success)

			curr_books = refservice.list_books(self.db, 1)
			added_books = set(curr_books) - set(initial_books)
			self.assertEqual(len(added_books), 1)

			tags = refservice.get_tags_for_ref(self.db, "book", added_books.pop().id)
			self.assertEqual(len(tags), 1)

			tag = tags.pop()
			self.assertEqual(tag.id, 1)
			self.assertEqual(tag.name, 'test tag 1')
