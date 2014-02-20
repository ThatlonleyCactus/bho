import xml.etree.ElementTree as ET;
import pymysql;
import sys;

conn = pymysql.connect(host="jim.dardenhome.com", port=3306, user="liam", passwd="", db="bible_history", charset="utf8");
curs = conn.cursor();
curs.execute("TRUNCATE TABLE web_verse");
#curs.close();

def getVerses(chapter):
	verses = [];
	inVerse = False;
	verseNumber = 0;
	verseText = "";

	for elem in chapter.iter():
		if (elem.tag == "v"):
			verseNumber = elem.attrib["id"];

		if (elem.tail != None):
			verseText += elem.tail.replace("\t", '').replace("\n", '');

		if (elem.tag == "wj"):
			verseText += elem.text.replace("\t", '').replace("\n", '');

		if (elem.tag == "ve"):
			verses.append([verseNumber, verseText]);
			verseText = "";
			verseNumber = 0;


	return verses;


def importXML():
	tree = ET.parse("eng-web_usfx.xml");
	rootElem = tree.getroot();

	i = 0;
	isOldTest = 'Y';
	bookOrder = 1;
	for book in rootElem.findall("book"):
		i += 1;
		if (i == 1 or i==86):
			continue; # skip past preface and glossary 
		if (i > 40 and i < 59): # skip apocrypha
			continue;
		if (i > 40):
			isOldTest = 'N';
			bookOrder = i - 19;
		else:
			isOldTest = 'Y';
			bookOrder = i - 1;


		currentChapter = 0;
		inChapter = False;
		tocs = book.findall("toc");
		for toc in tocs:
			if (toc.attrib["level"] == "2"):
				currentBookName = toc.text.replace("\n", "");
				break;

		for elem in book.iter():
			if (elem.tag == "c"):
				# inChapter = True;
				# currentVerse = 0;
				currentChapter = elem.attrib["id"];
				for verse in getVerses(elem):
					print(currentBookName + " " + str(currentChapter) + ":" + str(verse[0]) + " - " + verse[1]);
					curs.execute("INSERT INTO bible_history.web_verse(book, chapter, verse, verse_text, book_order, ot) " + 
						"VALUES ('" + currentBookName + "', " + str(currentChapter) + ", " + str(verse[0]) + ",'" + 
							str(verse[1].replace("'", "\\'")) + "', " + str(bookOrder) + ", '" + isOldTest + "')");

			# if (elem.tag == "ce"):
			# 	inChapter = False;

			# if (elem.tag == "p" and inChapter):
			# 	for verse in getVerses(elem):
			# 		print(currentBookName + " " + str(currentChapter) + ":" + str(verse[0]) + " - " + verse[1]);
			# 		curs.execute("INSERT INTO bible_history.web_verse(book, chapter, verse, verse_text, book_order, ot) " + 
			# 			"VALUES ('" + currentBookName + "', " + str(currentChapter) + ", " + str(verse[0]) + ",'" + 
			# 				str(verse[1].replace("'", "\\'")) + "', " + str(bookOrder) + ", '" + isOldTest + "')");

importXML();
quit();