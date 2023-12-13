from pybtex.database.input import bibtex
import bibtexparser

def from_doi_entry_to_database(entry, user_id,request):
	bib_data = _dict_from_doi_entry(entry).entries_dict
	data = {}
	data['cite_id']=request.form['cite_id']
	for key in bib_data:
		bib_data = bib_data[key]
	data['ENTRYTYPE']=bib_data['ENTRYTYPE']
	if bib_data['ENTRYTYPE']=="article":
		keys = ["author", "title", "journal", "year", "volume", "start_page", "end_page"]
		for key in keys:
			if key in bib_data:
				data[key] = bib_data[key]
		data["user_id"] = user_id
		pages = bib_data["pages"].split("–")
		data["start_page"] = pages[0]
		data["end_page"] = pages[1]
	elif bib_data['ENTRYTYPE']=="book":
		keys = ["author", "title", "year", "publisher", "start_page", "end_page"]
		for key in keys:
			if key in bib_data:
				data[key] = bib_data[key]
		data["user_id"] = user_id
		data["start_page"] = request.form['start_page']
		data["end_page"] = request.form['end_page']
	elif bib_data['ENTRYTYPE']=="inproceedings":
		keys = ["author", "title", "booktitle", "year", "editor", "start_page", "end_page"]
		for key in keys:
			if key in bib_data:
				data[key] = bib_data[key]
		data["user_id"] = user_id
		data["start_page"] = request.form['start_page']
		data["end_page"] = request.form['end_page']
	return data

def _dict_from_doi_entry(entry):
	return bibtexparser.loads(entry)
	