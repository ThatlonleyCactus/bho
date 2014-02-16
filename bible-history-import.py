import xml.etree.ElementTree as ET
import pymysql
import sys
import codecs
import unicodedata
import re


TAG_RE = re.compile(r'<[^>]+>')


def stripTags(text):
	return TAG_RE.sub('', text)



# for a given book.chapter.verse or book.chapter
# reference, return the final number (chapter or verse)
# e.g. Gen.1.1 or Exo.2 
def getNumberFromReference(reference):
	referenceNumber = reference[reference.rfind(".")+1:]
	return referenceNumber



def getVerses(paragrph):
	verses = []

	verseTagIndex = 1;
	while (verseTagIndex > 0):
		verseTagIndex = paragraph.find('<verse sID="', verseTagIndex)
		if (verseTagIndex == -1):
			break

		referenceStartIndex = verseTagIndex + 12
		referenceEndIndex = paragraph.find('"', referenceStartIndex)

		reference = paragraph[referenceStartIndex:referenceEndIndex]
		print ("Verse=" + getNumberFromReference(reference))
		verseTextStartIndex = paragraph.find('/>', verseTagIndex) + 2

		verseTextEndIndex = paragraph.find('<verse sID="', verseTextStartIndex)

		if (verseTextEndIndex == -1):
			verseText = paragraph[verseTextStartIndex:]
		else: 
			verseText = stripTags(paragraph[verseTextStartIndex:verseTextEndIndex])

		print (verseText)

		verseTagIndex += 1
	return ""


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