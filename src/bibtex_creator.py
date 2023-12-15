import refservice

def write_bibtex_file(db, user_id, output_file):
	books, articles, inproceedings = refservice.list_references(db, user_id)
	entries = []

	for book in books:
		entries.append(book_to_bibtex(book))
	for article in articles:
		entries.append(article_to_bibtex(article))
	for inproceeding in inproceedings:
		entries.append(inproceeding_to_bibtex(inproceeding))

	with open(output_file, 'w', encoding="utf8") as f:
		for entry in entries:
			f.write(entry)
			f.write('\n\n')

def book_to_bibtex(book):
	entry = '@book{'
	entry += book.cite_id + ',\n'
	entry += '  author = {' + book.author + '},\n'
	entry += '  title = {' + book.title + '},\n'
	entry += '  year = {' + str(book.year) + '},\n'
	entry += '  publisher = {' + book.publisher + '},\n'
	entry += '  pages = {' + str(book.start_page) + '--'+ str(book.end_page) + '},\n'
	entry += '}\n'
	return entry

def article_to_bibtex(article):
	entry = '@article{'
	entry += article.cite_id + ',\n'
	entry += '  author = {' + article.author + '},\n'
	entry += '  title = {' + article.title + '},\n'
	entry += '  journal = {' + article.journal + '},\n'
	entry += '  year = {' + str(article.year) + '},\n'
	entry += '  volume = {' + str(article.volume) + '},\n'
	entry += '  pages = {' + str(article.start_page) + '--'+ str(article.end_page) + '},\n'
	entry += '}\n'
	return entry

def inproceeding_to_bibtex(inproceeding):
	entry = '@inproceedings{'
	entry += inproceeding.cite_id + ',\n'
	entry += '  author = {' + inproceeding.author + '},\n'
	entry += '  title = {' + inproceeding.title + '},\n'
	entry += '  year = {' + str(inproceeding.year) + '},\n'
	entry += '  booktitle = {' + inproceeding.booktitle + '},\n'
	entry += '  pages = {' + str(inproceeding.start_page) + '--'+ str(inproceeding.end_page) + '},\n'
	entry += '}\n'
	return entry
