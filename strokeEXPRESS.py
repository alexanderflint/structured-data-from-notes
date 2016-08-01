#!/usr/bin/env python

# Parser program to import csv file containing free text note 
# with flagged enumeration content that extracts and exports 
# structured data as new csv file.
#

# Copyright Alexander C. Flint, MD, PhD
# Under MIT License - See LICENSE doc:
# https://github.com/alexanderflint/structured-data-from-notes

# @neuroicudoc

import re
import csv

MRN_HEADER = 'PAT_MRN_ID'
DATE_HEADER = 'notedate'
NOTE_HEADER = 'ConcatenatedText'
    
def SQLtagIsPresent(totalString):
    if re.search('regstrkdatnte92tkL76s3', totalString):
        return True
    else:
        return False

def remove_prefix(s, prefix):
    """ Removes string prefix from begining of string s. """
    return s[len(prefix):] if s.startswith(prefix) else s

def remove_suffix(s, suffix):
    """ Removes string suffix from end of string s. """
    return s[:len(s)-len(suffix)] if s.endswith(suffix) else s    
    
def extract(totalString, beginString, endString):
    """ Takes in totalString, beginString, and endString. If there is a match to the pattern:
        beingString ...any text... endString, capture the ...any text... portion, extract any
        integer characters in this text, and return the integer characters (as a string). """
    if re.search((beginString + r'.+' + endString), totalString):
        searchObject = re.search((beginString + r'.+' + endString), totalString)
        searchHit = remove_suffix(remove_prefix(searchObject.group(0), beginString), endString)
        intString = ''
        for character in searchHit:
            try:
                # check if character is an integer, and if so, add it to intString
                if character == str(int(character)):
                    intString += character
            # if it is not an integer, taking int() will raise a ValueError, so except this and keep going:
            except ValueError:
                pass
        if len(intString) > 0:
            intStringReturn = intString
        # handle the exception of no integer characters in searchHit by returning (777777 + searchHit text)
        else:    
            intStringReturn = '777777 _ ' + intString
    else:
        # handle the exception of no match to flanking text by returning 888888:
        intStringReturn = '888888'
    return intStringReturn

def convertCSVtoDataList(fileName):
    # open the CSV file and convert the contents into list of lists called dataList:
    dataList = []
    with open(fileName, 'rb') as csvfile:
        f = csv.reader(csvfile)
        for row in f:
            mrn = row[2]
            noteDate = row[3]
            noteText = row[4]
            if (mrn == MRN_HEADER) or (noteDate == DATE_HEADER) or (noteText == NOTE_HEADER):
                print('Skipped a header row in the input file.')
            else:    
                dataList.append([mrn, noteDate, noteText])
        print('Processed ' + str(len(dataList)) + ' rows from the input file.')
        return dataList

def removecsv(name):
    newname = re.sub('\.csv$', '', name)
    return newname

def convertToTimeStamp(timeString):
    if len(timeString)==3:
        timeOutput = timeString[0:1]+':'+timeString[1:3]
    if len(timeString)==4:
        timeOutput = timeString[0:2]+':'+timeString[2:4]
    # handle exception of timeString being any length other than 3 or 4 characters by returning 999999 + timeString text
    else:
        timeOutput = '999999 _ ' + timeString
    return timeOutput
        
def main():
    print('********************************************************************************')
    print('This program parses data for the Stroke EXPRESS Telemedicine Project')
    print('********************************************************************************')
    print('''
    
    The data in the input CSV file must contain exactly 5 columns in the
    following order, with these exact column header names in the top row:
    
    <blank header> rownums | encdate | PAT_MRN_ID | notedate | ConcatenatedText
    
        ''')
    print('********************************************************************************')
    fileName = raw_input('Name of the CSV file (include .csv extension) ->  ')
    fileNameWithoutCSV = removecsv(fileName)
    outputCSVfileName = fileNameWithoutCSV + "_output.csv"
    dataList = convertCSVtoDataList(fileName)
    #write column titles to first row of file
    columnTitleList = ['MRN', 'noteDate', 'lastSeenNormal', 'broughtInBy', 'strokeAlert', 'NIHSSscore', 'NIHSStime', 'bleed', 'CTA', 'largeArteryOcclusion', 'strokeLocation', 'tpaGiven', 'EST']
    filewriter = csv.writer(open(outputCSVfileName, 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(columnTitleList)

    rowCounter = 0
    for i in dataList:
        allFields = dataList[rowCounter]
        mrn = int(allFields[0])
        noteDate = allFields[1]
        noteText = allFields[2]
        # extract each of the integer data fields from noteText:
        if SQLtagIsPresent(noteText):
            lastSeenNormal = convertToTimeStamp(extract(noteText, "Last seen normal:", "varLSN"))
            broughtInBy = extract(noteText, "Brought in by:", "varBIB")
            strokeAlert = convertToTimeStamp(extract(noteText, "Stroke alert time:", "varAlert"))
            NIHSSscore = extract(noteText, "NIHSS score:", "varNIHS")
            NIHSStime = convertToTimeStamp(extract(noteText, "NIHSS time:", "varNIHT"))
            bleed = extract(noteText, "Bleed on CT:", "varBleed")
            CTA = extract(noteText, "CTA:", "varCTA")
            largeArteryOcclusion = extract(noteText, "Large artery occlusion:", "varLAO")
            strokeLocation = extract(noteText, "Stroke location:", "varSide")
            tpaGiven = extract(noteText, "tPA given:", "varTPA")
            EST = extract(noteText, "EST:", "varEST")
            valueList = [mrn, noteDate, lastSeenNormal, broughtInBy, strokeAlert, NIHSSscore, NIHSStime, bleed, CTA, largeArteryOcclusion, strokeLocation, tpaGiven, EST]
            filewriter.writerow(valueList)
        rowCounter += 1

    print('')
    pauseVarC = raw_input('Enter to quit ->  ')
    print('Quitting')
    
if __name__ == "__main__":
    main()

