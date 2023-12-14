from enum import Enum

class ResultState(Enum):
	success = 0
	duplicate_cite_id = 1
	doi_not_found = 2

def make_plural(name):
	if name[-1] == "s":
		return name

	return name + "s"

def get_column_names(ref_type):
	keys = {
		"inproceedings": ["cite_id", "author", "title", "year", "booktitle", "start_page", "end_page"],
		"articles": ["cite_id", "author", "title", "journal", "year", "volume", "start_page", "end_page"],
		"books":  ["cite_id", "author", "title", "year", "publisher", "start_page", "end_page"]
	}

	return keys[make_plural(ref_type)]
