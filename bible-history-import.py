import pymysql
import xml.etree.ElementTree as ET
import sys
import codecs
import unicodedata


def getChapterNumber(fullChapter):
	chapter = fullChapter[fullChapter.find(".")+1:]	 
	return chapter


def getVerseNumber(fullVerse):
	verse = fullVerse[fullVerse.rfind(".")+1:]
	return verse

conn = pymysql.connect(host="jim.dardenhome.com", # your host, usually localhost
					 port=3306,
                     user="liam", # your username
                     passwd="", # your password
                     db="bible_history") # name of the data base
curs = conn.cursor()
fp = open("web.osis.xml","r")
xml=fp.read()
rootElem = ET.fromstring(xml)
bookGroups = rootElem.findall(".//*[@type='bookGroup']")
groupNum = 0;
for bookGroup in bookGroups:
	groupNum += 1;
	if (groupNum == 2):
		continue
	if (groupNum == 1):
		isOldTest = 'Y'
	else:
		isOldTest = 'N'

	books = bookGroup.findall(".//*[@type='book']")
	bookOrder = 0;
	for book in books:
		try:
			currentBookName = book.find("{http://www.bibletechnologies.net/2003/OSIS/namespace}title").attrib.get("short")
			currentChapter = book.find("{http://www.bibletechnologies.net/2003/OSIS/namespace}chapter").attrib.get("sID")
		except:
			print("oops")
			continue

		paragraphs = book.findall("{http://www.bibletechnologies.net/2003/OSIS/namespace}p")
		for paragraph in paragraphs:
			print(ET.tostring(paragraph))
			quit()
			# for element in paragraph:
			# 	if element.tag == "{http://www.bibletechnologies.net/2003/OSIS/namespace}verse":
			# 		# <verse sID="Gen.1.1" osisID="Gen.1.1" />
			# 		# In the beginning <milestone type="x-noteStartAnchor" />God
			# 		# <note type="translation">The Hebrew word rendered “God” is “Elohim.” After “God,” 
			# 		# the Hebrew has the two letters “Aleph Tav” (the first and last letters of the 
			# 		# Hebrew alphabet) as a grammatical marker.</note> created the heavens and the earth.
			# 		# <verse eID="Gen.1.1" />

			# 		# see if this is the start of the verse or end
			# 		try:
			# 			newVerse = element.attrib.get("sID")
			# 		except:
			# 			# if there is no sID then this is the eID and we can ignore it
			# 			continue

			# 		# we just want the text 
			# 		print(str(currentBookName) + ":" + str(currentChapter) + ":" + str(currentVerse))


	# 			currentVerse = verse.attrib["id"]
	# 			currentVerseText = childElem.text
	# 			print (currentBookName + ":" + currentChapter + ":" + currentVerse)
	# 			curs.execute("INSERT INTO bible_history.web_verse(book, chapter, verse, verse_text, book_order, ot) " +
	# 				"VALUES ('" + currentBookName + "', " + str(currentChapter) + ", " + str(currentVerse) + ", 'dummy', " + str(bookOrder) + ", '" + isOldTest + "')")
	# 			break