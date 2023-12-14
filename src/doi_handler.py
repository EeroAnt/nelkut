import bibtexparser
import refservice

def from_doi_entry_to_database(entry, user_id, request):
	bib_data = list(bibtexparser.loads(entry).entries_dict.values())[0]

	columns = {
		"user_id": user_id,
		"cite_id": request.form["cite_id"],
	}

	for key in refservice.get_keys(bib_data["ENTRYTYPE"]):
		if key in bib_data:
			columns[key] = bib_data[key]

	if bib_data["ENTRYTYPE"] == "article":
		columns["start_page"], columns["end_page"] = bib_data["pages"].split("–")
	else:
		columns["start_page"] = request.form["start_page"]
		columns["end_page"] = request.form["end_page"]

	return columns, bib_data["ENTRYTYPE"]
