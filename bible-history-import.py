import xml.etree.ElementTree as ET;
import pymysql;
import sys;
import codecs;

conn = pymysql.connect(host="jim.dardenhome.com", port=3306, user="liam", passwd="", db="bible_history", charset="utf8");
conn.charset="utf8";
curs = conn.cursor();
curs.execute("TRUNCATE TABLE web_verse");



def getVerses(book):
	inVerse = False;
	verses = [];
	inVerse = False;
	inVerse = False;
	verseNumber = 0;
	verseText = "";
	chapterNumber = 0;

	for child in book.iter():
		if (child.tag == "c"):
			chapterNumber = child.attrib["id"];

		if (child.tag == "v"):
			inVerse = True;
			verseNumber = child.attrib["id"];

		if (inVerse):
			if (child.text != None):
				if (child.tag == "f"):
					verseText += " <note>" + child.text.replace("\t", '').replace("\n", '')  + "</note> ";
				else:
					verseText += child.text.replace("\t", '').replace("\n", '');

			if (child.tail != None):
				verseText += child.tail.replace("\t", '').replace("\n", '');


		if (child.tag == "ve"):
			inVerse = False;
			tup = [chapterNumber, verseNumber, verseText];
			verses.append(tup);

			verseText = "";
			verseNumber = 0;
			continue;



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

		for verse in getVerses(book):
			print(currentBookName + " " + str(verse[0]) + ":" + str(verse[1]) + " - " + verse[2]);
			curs.execute("INSERT INTO bible_history.web_verse(book, chapter, verse, verse_text, book_order, ot) " + 
				"VALUES ('" + currentBookName + "', " + str(verse[0]) + ", " + str(verse[1]) + ",'" + 
					str(verse[2].replace("'", "\\'")) + "', " + str(bookOrder) + ", '" + isOldTest + "')");

importXML();
quit();