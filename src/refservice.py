from collections import namedtuple
import requests
from sqlalchemy.sql import text
from doi_handler import from_doi_entry_to_database
from util import ResultState, get_column_names

Tag = namedtuple('Tag', ['id', 'name'])

def __add_tags(db, table_name, inserted_id, request, user_id):
	sql = f"INSERT INTO tags_to_{table_name} (tag_id, {table_name[:-1]}_id) VALUES (:tag_id, :ref_id)"

	for tag in get_tags_for_user(db, user_id):
		if request.form.get(str(tag.id)) == 'on':
			db.session.execute(text(sql), {"tag_id": tag.id, "ref_id": inserted_id})

def __user_has_ref_with_cite_id(db, user_id, cite_id):
	for table in ["books", "articles", "inproceedings"]:
		sql = f"SELECT * FROM {table} WHERE cite_id=:cite_id AND user_id=:user_id"

		if db.session.execute(text(sql), {"cite_id": cite_id, "user_id": user_id}).fetchall():
			return True

	return False

def __insert(db, table_name, request, user_id):
	if __user_has_ref_with_cite_id(db, user_id, request.form["cite_id"]):
		return ResultState.duplicate_cite_id

	keys = get_column_names(table_name)
	key_str = ', '.join(keys)
	val_str = ', '.join(':' + key for key in keys)
	sql = f"INSERT INTO {table_name} ({key_str}, user_id) VALUES ({val_str}, :user_id) RETURNING id"

	columns = __handle_missing_numbers({key: request.form[key] for key in keys})
	columns["user_id"] = user_id
	inserted_id = db.session.execute(text(sql), columns).fetchone()[0]

	__add_tags(db, table_name, inserted_id, request, user_id)
	db.session.commit()

	return ResultState.success

def add_inproceeding_to_database(db, request, user_id):
	return __insert(db, "inproceedings", request, user_id)

def add_article_to_database(db, request, user_id):
	return __insert(db, "articles", request, user_id)

def add_book_to_database(db, request, user_id):
	return __insert(db, "books", request, user_id)

def add_new_tag(db, request, user_id):
	sql = "INSERT INTO tags (name, user_id) VALUES (:name, :user_id)"
	db.session.execute(text(sql), {"name": request.form["name"], "user_id": user_id})
	db.session.commit()

def get_tags_for_user(db, user_id):
	sql = "SELECT id, name FROM tags WHERE user_id=:user_id"
	results = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
	return [Tag(*args) for args in results]

def get_tags_for_ref(db, ref_type, ref_id):
	sql = f"""SELECT id, name FROM tags t JOIN tags_to_{ref_type}s t2r
		ON t.id = t2r.tag_id WHERE t2r.{ref_type}_id = :ref_id"""

	results = db.session.execute(text(sql), {"ref_id": ref_id}).fetchall()
	return [Tag(*args) for args in results]

def list_books(db, user_id):
	sql = f"SELECT * FROM books WHERE user_id={user_id}"
	books = db.session.execute(text(sql)).fetchall()
	return books

def list_articles(db, user_id):
	sql = f"SELECT * FROM articles WHERE user_id={user_id}"
	articles = db.session.execute(text(sql)).fetchall()
	return articles

def list_inproceedings(db, user_id):
	sql = f"SELECT * FROM inproceedings WHERE user_id={user_id}"
	inproceedings = db.session.execute(text(sql)).fetchall()
	return inproceedings

def list_references(db, user_id):
	if user_id is not None:
		books = list_books(db, user_id)
		articles = list_articles(db, user_id)
		inproceedings = list_inproceedings(db, user_id)
	else:
		books, articles, inproceedings = [], [], []
	return books, articles, inproceedings

def __handle_missing_numbers(columns):
	for key in columns:
		if key in ["start_page", "end_page", "volume", "year"]:
			if columns[key] == "":
				columns[key] = None
	return columns
