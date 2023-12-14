from enum import Enum
from sqlalchemy.sql import text
from flask import render_template
from habanero import cn
from doi_handler import from_doi_entry_to_database
import requests

class ResultState(Enum):
	SUCCESS = 0
	DUPLICATE_CITE_ID = 1
	DOI_NOT_FOUND = 2

def __make_plural(name):
	if name[-1] == "s":
		return name

	return name + "s"

def get_keys(ref_type):
	keys = {
		"inproceedings": ["cite_id", "author", "title", "year", "booktitle", "start_page", "end_page"],
		"articles":      ["cite_id", "author", "title", "journal", "year", "volume", "start_page", "end_page"],
		"books":         ["cite_id", "author", "title", "year", "publisher", "start_page", "end_page"]
	}

	return keys[__make_plural(ref_type)]

class Tag:
	def __init__(self, id, name):
		self.id = id
		self.name = name

def __add_tags(db, table_name, inserted_id, request, user_id):
	sql = f"INSERT INTO tags_to_{table_name} (tag_id, {table_name[:-1]}_id) VALUES (:tag_id, :ref_id)"

	for tag in get_tags_for_user(db, user_id):
		if request.form.get(str(tag.id)) == 'on':
			db.session.execute(text(sql), {"tag_id": tag.id, "ref_id": inserted_id})

def __insert(db, table_name, request, user_id):
	if not check_users_cite_id_duplicate(request.form["cite_id"], db, user_id):
		return ResultState.DUPLICATE_CITE_ID

	keys = get_keys(table_name)
	key_str = ', '.join(keys)
	val_str = ', '.join(':' + key for key in keys)
	sql = f"INSERT INTO {table_name} ({key_str}, user_id) VALUES ({val_str}, :user_id) RETURNING id"

	keys_dict = __handle_input({key: request.form[key] for key in keys})
	keys_dict["user_id"] = user_id
	inserted_id = db.session.execute(text(sql), keys_dict).fetchone()[0]

	__add_tags(db, table_name, inserted_id, request, user_id)
	db.session.commit()

	return ResultState.SUCCESS

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
	sql = f"SELECT id, name FROM tags t JOIN tags_to_{ref_type}s t2r ON t.id = t2r.tag_id WHERE t2r.{ref_type}_id = :ref_id"
	results = db.session.execute(text(sql), {"ref_id": ref_id}).fetchall()
	return [Tag(*args) for args in results]

def add_from_doi(db, request, user_id):
	try:
		entry = cn.content_negotiation(ids = request.form["doi"])
	except requests.exceptions.HTTPError:
		return ResultState.DOI_NOT_FOUND

	columns, ref_type = from_doi_entry_to_database(entry, user_id, request)

	if not check_users_cite_id_duplicate(columns["cite_id"], db, user_id):
		return ResultState.DUPLICATE_CITE_ID

	key_str = ', '.join(columns.keys())
	val_str = ', '.join(':' + key for key in columns)
	sql = f"INSERT INTO {__make_plural(ref_type)} ({key_str}) VALUES ({val_str})"

	db.session.execute(text(sql), columns)
	db.session.commit()
	return ResultState.SUCCESS

def check_users_cite_id_duplicate(cite_id, db, user_id):
	sql = "SELECT id FROM users WHERE id=:user_id"
	if db.session.execute(text(sql), {"user_id":user_id}).fetchone()[0]:
		for i in ["books", "articles", "inproceedings"]:
			sql = f"SELECT * FROM {i} WHERE cite_id=:cite_id AND user_id=:user_id"
			check = db.session.execute(text(sql), {"cite_id":cite_id,"user_id":user_id}).fetchall()
			if check:
				return False
		return user_id
	return False

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

def __handle_input(input):
	for key in input:
		if key in ["start_page", "end_page","volume", "year"]:
			if input[key] == "":
				input[key] = None
	return input
