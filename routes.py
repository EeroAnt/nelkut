from flask import request, redirect, render_template, send_from_directory, session
from app import app
import refservice
import users
from db import db
from bibtex_creator import write_bibtex_file, sort_entries
import os

@app.route("/")
def index():
	if len(session) != 0:
		user_id = session["user_id"]
	else:
		user_id = None
	books, articles, inproceedings = refservice.list_references(db, user_id)
	return render_template("index.html", books = books, articles = articles, inproceedings = inproceedings)


@app.route("/add", methods=["GET"])
def add():
	return render_template("add_reference.html")

@app.route("/add_inproceeding", methods=["GET", "POST"])
def add_inproceeding():
	if request.method == "GET":
		return render_template("add_inproceeding_reference.html")
	user_id = session["user_id"]
	refservice.add_inproceeding_to_database(db, request, user_id)

	return redirect("/")

@app.route("/add_article", methods=["GET", "POST"])
def add_article():
	if request.method == "GET":
		return render_template("add_article_reference.html")
	user_id = session["user_id"]
	refservice.add_article_to_database(db, request, user_id)

	return redirect("/")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
	if request.method == "GET":
		return render_template("add_book_reference.html")

	user_id = session["user_id"]
	refservice.add_book_to_database(db, request, user_id)

	return redirect("/")

@app.route("/bibtex")
def bibtex():
	write_bibtex_file(sort_entries(), "bibtex.bib")
	return redirect("/download")

@app.route("/download")
def download():
	return send_from_directory(app.root_path, "bibtex.bib", as_attachment=True)

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(db, username, password):
			return redirect("/")
		else:
			return render_template("error.html", message="Wrong username or password")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	if request.method == "POST":
		username = request.form["username"]
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if password1 != password2:
			return render_template("error.html", message="Passwords do not match")
		if users.register(db, username, password1):
			return redirect("/")
		else:
			return render_template("error.html", message="Registration failed")