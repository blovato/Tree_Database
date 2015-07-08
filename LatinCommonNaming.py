#       Clean Up Latin and Common Names of Trees
#       Brenten Lovato
#       San Francisco,
#       Dept. of Public Works
#       7.1.15
#
#       USAGE: Searches field of tree.shp and arranges 
#              data in a standardized format

#       import and setup
print "***** RUNNING Latin and Common Names SCRIPT *****"
print "Importing Modules..."
import arcpy, sys
from arcpy import env
from math import sin, cos, radians, pi
env.overwriteOutput = 1

#       input variables and assign workspace
print "Setting Environment..."
input_ws = "C:\Users\blovato\Desktop\SFGISData_Brenten\PyTest"
input_fc = "Trees_June2015_sunset_movedXY_10.shp"
env.workspace = input_ws

#			function to check existing field
def FieldExist(featureclass, fieldname):
   fieldList = arcpy.ListFields(featureclass, fieldname)
   fieldCount = len(fieldList)
   if (fieldCount == 1):
      return True
   else:
      return False

#        add missing fields
print "Checking for existing fields..."
if (not FieldExist(input_fc, "CommonName")):
   print "Adding 'CommonName' field..."
   arcpy.AddField_management(input_fc, "CommonName", "TEXT", "30", "30", "", "", "NULLABLE", "")
else:
   print "'CommonName' field already exists..."
if (not FieldExist(input_fc, "LatinName")):
   print "Adding 'LatinName' field..."
   arcpy.AddField_management(input_fc, "LatinName", "TEXT", "30", "30", "", "", "NULLABLE", "")
else:
   print "'LatinName' field already exists..."

#			loop through existing species list and cut it to place into new fields
print "Calculating fields..."
rows = arcpy.UpdateCursor(input_fc)
for row in rows:
   if " : " in row.qSpeciesTe:
      row.CommonName = row.qSpeciesTe.split(" : ")[1]
      row.LatinName = row.qSpeciesTe.split(" : ")[0]
      rows.updateRow(row)
   else:
      row.CommonName = row.qSpeciesTe
      row.LatinName = row.qSpeciesTe
      rows.updateRow(row)
   del row
del rows

print "***** FINISHED Latin and Common Names SCRIPT *****"
