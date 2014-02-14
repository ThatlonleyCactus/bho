import pymysql
import xml.etree.ElementTree as ET
import sys
import codecs

conn = pymysql.connect(host="jim.dardenhome.com", # your host, usually localhost
					 port=3306,
                     user="liam", # your username
                     passwd="", # your password
                     db="bible_history") # name of the data base
curs = conn.cursor()
fp = codecs.open("WEB/eng-web_usfx.xml","r", "utf-8")
xml=fp.read()
#rootElem = ET.parse(fp)
rootElem = ET.fromstring(xml)
books = rootElem.findall("book")
bookOrder = 0;
for book in books:
	bookOrder += 1;
	if (bookOrder > 39):
		isOldTest = 'Y'
	else:
		isOldTest = 'N'

	#currentChapter = 0;
	for childElem in book:
		if (childElem.tag == "toc" and childElem.attrib["level"] == "2"):
			currentBookName = childElem.text.strip();
		if (childElem.tag == "c"):
			currentChapter = childElem.attrib["id"]
		if (childElem.tag == "p"):
			verses = childElem.findall("v")
			for verse in verses:
				currentVerse = verse.attrib["id"]
				#currentVerseText = childElem.text
				print (currentBookName + ":" + currentChapter + ":" + currentVerse)
				curs.execute("INSERT INTO bible_history.web_verse(book, chapter, verse, verse_text, book_order, ot) " +
					"VALUES ('" + currentBookName + "', " + str(currentChapter) + ", " + str(currentVerse) + ", 'dummy', " + str(bookOrder) + ", '" + isOldTest + "')")
				break