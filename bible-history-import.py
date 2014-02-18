import xml.etree.ElementTree as ET;
import pymysql;
import sys;

conn = pymysql.connect(host="jim.dardenhome.com", # your host, usually localhost
					 port=3306,
                    user="liam", # your username
                    passwd="", # your password
                    db="bible_history") # name of the data base
curs = conn.cursor();


# for a given book.chapter.verse or book.chapter
# reference, return the final number (chapter or verse)
# e.g. Gen.1.1 or Exo.2 
def getNumberFromReference(reference):
	return reference[reference.rfind(".")+1:];



def getVerses(paragraph):
	verses = [];
	inVerse = False;
	verseNumber = 0;
	verseText = "";

	for elem in paragraph.iter():
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

			
			



tree = ET.parse("eng-web_usfx.xml");
rootElem = tree.getroot();

i = 0;
for book in rootElem.findall("book"):
	i += 1;
	if (i > 39 and i < 60): # skip apacraphal
		continue;
	currentChapter = 0;
	inChapter = False;
	tocs = book.findall("toc");
	for toc in tocs:
		if (toc.attrib["level"] == "2"):
			currentBookName = toc.text.replace("\n", "");
			break;
	for elem in book.iter():
		if (elem.tag == "c"):
			inChapter = True;
			currentVerse = 0;
			currentChapter = elem.attrib["id"];
		if (elem.tag == "ce"):
			inChapter = False;

		if (elem.tag == "p" and inChapter):
			for verse in getVerses(elem):
				print(currentBookName + " " + str(currentChapter) + ":" + str(verse[0]) + " - " + verse[1]);
			# curs.execute("INSERT INTO bible_history.web_verse(book, chapter, verse, verse_text, book_order, ot) " +
 		# 	"VALUES ('" + currentBookName + "', " + str(currentChapter) + ", " + str(verse[0]) + ", str(verse[1]), " + str(bookOrder) + ", '" + isOldTest + "')")			

			#for pelem in elem.itertext(): # dig into the chapter
			#	print(pelem);
			#	continue;
			#	print(pelem.text);
			#	if (pelem.tag == "v"):
			#		currentVerse = pelem.attrib["id"];
			#		print(currentBookName + " " + currentChapter + ":" + currentVerse);	
			#		print(pelem.text);
print(i);
				



