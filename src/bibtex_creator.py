from flask import session
from db import db
from refservice import list_references

def sort_entries():
	books, articles, inproceedings = list_references(db, session["user_id"])
	entries = []
	for book in books:
		entries.append(to_bibtex(book, "book"))
	for article in articles:
		entries.append(to_bibtex(article, "article"))
	for inproceeding in inproceedings:
		entries.append(to_bibtex(inproceeding, "inproceeding"))
	return entries

def write_bibtex_file(entries, output_file):
	with open(output_file, 'w', encoding="utf8") as f:
		for entry in entries:
			f.write(entry)
			f.write('\n\n')

def to_bibtex(entry, entry_type):
	# Create a dictionary of entry types and their corresponding fields
	entry_fields = {
		"book": {"type": "@book", "special_fields": [("publisher", entry.publisher)]},
		"article": {"type": "@article", "special_fields": [("journal", entry.journal), ("volume", str(entry.volume))]},
		"inproceeding": {"type": "@inproceedings", "special_fields": [("booktitle", entry.booktitle)]}
	}

	# Choose the correct fields for the given entry type
	fields = entry_fields[entry_type]

	# Create the bibtex entry
	bibtex_entry = f"{fields['type']}{{{entry.cite_id}},\n"
	bibtex_entry += f"  author = {{{entry.author}}},\n"
	bibtex_entry += f"  title = {{{entry.title}}},\n"
	bibtex_entry += f"  year = {{{entry.year}}},\n"
	for field, value in fields["special_fields"]:
		bibtex_entry += f"  {field} = {{{value}}},\n"
	bibtex_entry += f"  pages = {{{entry.start_page}--{entry.end_page}}},\n"
	bibtex_entry += "}\n"

	return bibtex_entry