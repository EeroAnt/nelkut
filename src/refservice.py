from sqlalchemy.sql import text
from flask import render_template
from habanero import cn
from doi_handler import from_doi_entry_to_database

def __insert(db, table_name, keys, request, user_id):
	colon = ':'
	key_str = ', '.join(keys)
	val_str = ', '.join(colon + key for key in keys)
	sql = f"INSERT INTO {table_name} ({key_str}, user_id) VALUES ({val_str}, :user_id)"

	keys_dict = {key: request.form[key] for key in keys}
	keys_dict = __handle_input(keys_dict)
	keys_dict["user_id"] = user_id
	db.session.execute(text(sql), keys_dict)
	db.session.commit()

def __insert_from_doi(db, table_name, data):
	colon = ':'
	keys = data.keys()
	key_str = ', '.join(keys)
	val_str = ', '.join(colon + key for key in keys)
	sql = f"INSERT INTO {table_name} ({key_str}) VALUES ({val_str})"

	db.session.execute(text(sql), data)
	db.session.commit()

def add_inproceeding_to_database(db, request, user_id):
	keys = ["cite_id", "author", "title", "year", "booktitle", "start_page", "end_page"]
	if check_users_cite_id_duplicate(request.form["cite_id"], db, user_id):
		__insert(db, "inproceedings", keys, request, user_id)
	else:
		return render_template("error.html", message="You already have an reference with this cite_id.")

def add_article_to_database(db, request, user_id):
	keys = ["cite_id", "author", "title", "journal", "year", "volume", "start_page", "end_page"]
	if check_users_cite_id_duplicate(request.form["cite_id"], db, user_id):
		__insert(db, "articles", keys, request, user_id)
	else:
		return render_template("error.html", message="You already have an reference with this cite_id.")

def add_book_to_database(db, request, user_id):
	keys = ["cite_id", "author", "title", "year", "publisher", "start_page", "end_page"]
	if check_users_cite_id_duplicate(request.form["cite_id"], db, user_id):
		__insert(db, "books", keys, request, user_id)
	else:
		return render_template("error.html", message="You already have an reference with this cite_id.")
	
def add_from_doi(db, request, user_id):
	try:
		entry = cn.content_negotiation(ids = request.form["doi"])
		data = from_doi_entry_to_database(entry, user_id, request)
		if check_users_cite_id_duplicate(data["cite_id"], db, user_id):
			if data["ENTRYTYPE"]=="article":
				del data["ENTRYTYPE"]
				__insert_from_doi(db, "articles", data)
			elif data["ENTRYTYPE"]=="book":
				del data["ENTRYTYPE"]
				__insert_from_doi(db, "books", data)
			elif data["ENTRYTYPE"]=="inproceedings":
				del data["ENTRYTYPE"]
				__insert_from_doi(db, "inproceedings", data)
	except:
		return render_template("error.html", message="Invalid DOI.")

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