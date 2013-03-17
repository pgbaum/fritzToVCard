#!/usr/bin/env python

#
# Simple script to convert a telephone book from a Fritz!Box to vCard
#
# (c) 2013 P.G. Baum
#
# This code is Public Domain
# Do whatever you want with it.
#

import argparse
import codecs
import xml.etree.ElementTree as ET

# number is a child of person or of telephony
def processNumbers( fp, el, countryCode, areaCode ):
   telType = { "mobile": "CELL", "work": "WORK", "home": "HOME" }
   for number in el.findall( 'number' ):
      if number.text:
         tType = telType[number.attrib["type"]]
         nr = number.text.strip()
         if len( areaCode ) and nr[0] != "+" and nr[0] != "0":
            nr = areaCode + " / " + nr
         if len( countryCode ) and nr[0] != "+" and nr[0:1] != "00":
            if nr[0] == "0":
               nr = nr[1:]
            nr = "+" + countryCode + " " + nr
         fp.write( "TEL;TYPE=%s:%s\n" % (tType, nr) )

def processContact( fp, contact, countryCode, areaCode ):
   el = contact.find( "person" )
   name = el.find( 'realName' ).text
   print "Writing", name
   fp.write( "BEGIN:VCARD\nVERSION:3.0\nFN:%s\n" % (name,) )
   nameList = name.split( ' ' )
   txt = nameList[-1] + ";" + " ".join( nameList[0:-1] )
   fp.write( "N:%s;;;\n" % (txt,) )
   processNumbers( fp, contact, countryCode, areaCode )
   for child in contact.findall( "telephony" ):
      processNumbers( fp, child, countryCode, areaCode )
   fp.write( "END:VCARD\n\n" )

def doIt( inFile, outFile, countryCode, areaCode ):
   root = ET.parse( inFile ).getroot()
   fp = codecs.open( outFile, mode="w", encoding="utf-8" )
   for phoneBook in root.iter( 'phonebook' ):
      for contact in phoneBook.iter( 'contact' ):
         processContact( fp, contact, countryCode, areaCode )

parser = argparse.ArgumentParser(
      description = 'Convert Fritz-Box telephone list to vCards' )
parser.add_argument( "--inFile", help="input file" )
parser.add_argument( "--outFile", help="output file" )
parser.add_argument( "--countryCode", help="Prefix for telephone number",
      default="" )
parser.add_argument( "--areaCode", help="Prefix for telephone number",
      default="" )

args = parser.parse_args()

doIt( args.inFile, args.outFile, args.countryCode, args.areaCode )

