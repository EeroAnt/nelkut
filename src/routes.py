from flask import request, redirect, render_template, send_from_directory, session
from app import app
import refservice
import users
from db import db
from bibtex_creator import write_bibtex_file

def __redirect_back(result_state):
	match result_state:
		case refservice.ResultState.duplicate_cite_id:
			return render_template("error.html", message="You already have a reference with this cite ID")
		case refservice.ResultState.doi_not_found:
			return render_template("error.html", message="Could not find a reference with this DOI")

	return redirect("/")

def __get_tags(ref_type, ref_id):
	return ", ".join(tag.name for tag in refservice.get_tags_for_ref(db, ref_type, ref_id))

@app.route("/")
def index():
	if len(session) != 0:
		user_id = session["user_id"]
	else:
		user_id = None

	books, articles, inproceedings = refservice.list_references(db, user_id)

	return render_template("index.html",
		books=books,
		articles=articles,
		inproceedings=inproceedings,
		get_tags=__get_tags)

@app.route("/add", methods=["GET"])
def add():
	return render_template("add_reference.html")

@app.route("/add_inproceeding", methods=["GET", "POST"])
def add_inproceeding():
	user_id = session["user_id"]

	if request.method == "GET":
		return render_template("add_inproceeding_reference.html",
			tags=refservice.get_tags_for_user(db, user_id))

	result_state = refservice.add_inproceeding_to_database(db, request, user_id)
	return __redirect_back(result_state)

@app.route("/add_article", methods=["GET", "POST"])
def add_article():
	user_id = session["user_id"]

	if request.method == "GET":
		return render_template("add_article_reference.html",
			tags=refservice.get_tags_for_user(db, user_id))

	result_state = refservice.add_article_to_database(db, request, user_id)
	return __redirect_back(result_state)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
	user_id = session["user_id"]

	if request.method == "GET":
		return render_template("add_book_reference.html",
			tags=refservice.get_tags_for_user(db, user_id))

	result_state = refservice.add_book_to_database(db, request, user_id)
	return __redirect_back(result_state)

@app.route("/new_tag", methods=["GET", "POST"])
def new_tag():
	if request.method == "GET":
		return render_template("new_tag.html")

	user_id = session["user_id"]
	refservice.add_new_tag(db, request, user_id)

	return redirect("/")

@app.route("/add_from_doi", methods=["GET", "POST"])
def add_from_doi():
	user_id = session["user_id"]

	if request.method == "GET":
		return render_template("add_doi_reference.html", tags=refservice.get_tags_for_user(db, user_id))

	result_state = refservice.add_from_doi(db, request, user_id)
	return __redirect_back(result_state)

@app.route("/bibtex")
def bibtex():
	write_bibtex_file(db, session["user_id"], "bibtex.bib")
	return redirect("/download")

@app.route("/download")
def download():
	return send_from_directory(app.root_path, "bibtex.bib", as_attachment=True)

@app.route("/login", methods=["GET"])
def login_get():
	return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
	username = request.form["username"]
	password = request.form["password"]

	if users.login(db, username, password):
		return redirect("/")

	return render_template("error.html", message="Wrong username or password")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

@app.route("/register", methods=["GET"])
def register_get():
	return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
	username = request.form["username"]
	password1 = request.form["password1"]
	password2 = request.form["password2"]

	if password1 != password2:
		return render_template("error.html", message="Passwords do not match")

	if users.register(db, username, password1):
		return redirect("/")

	return render_template("error.html", message="Registration failed")
