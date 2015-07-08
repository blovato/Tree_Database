#       Tree Match
#       Brenten Lovato
#       San Francisco,
#       Dept. of Public Works
#       7.6.15
#
#       USAGE:  
#              
#              

#       import and setup
print "***** RUNNING Match Probablitity SCRIPT *****"

print "Importing Modules..."
import arcpy, sys
from arcpy import env

#       input variables and assign workspace
print "Setting Environment..."
env.workspace = r"C:\\Users\\blovato\\Desktop\\SFGISData_Brenten\\PyTest" # workspace
input_Davy = r"C:\\Users\\blovato\\Desktop\\SFGISData_Brenten\\PyTest\\Davy_Original_clip_sunset.shp" # Original Davy Tree Survey
input_DPW = r"C:\\Users\\blovato\\Desktop\\SFGISData_Brenten\\PyTest\\Trees_June2015_sunset_movedXY_10.shp" # DPW Trees after running algorith to move points
davy_buffer = r"C:\\Users\\blovato\\Desktop\\SFGISData_Brenten\\PyTest\\davy_buffer.shp" # buffer of Davy
davyBuff_joinDPW = r"C:\\Users\\blovato\\Desktop\\SFGISData_Brenten\\PyTest\\davyBuff_joinDPW.shp" # joining buffer to DPW Trees
distance = 15   # in feet
env.overwriteOutput = True

#       function to check existing field
def FieldExist(featureclass, fieldname):
   fieldList = arcpy.ListFields(featureclass, fieldname)
   fieldCount = len(fieldList)
   if (fieldCount == 1):
      return True
   else:
      return False

#        add missing fields
print "Checking for existing fields..."
if (not FieldExist(input_DPW, "match_prob")):
   print "Adding 'match_prob' field..."
   arcpy.AddField_management(input_DPW, "match_prob", "LONG", "30", "30", "", "", "NULLABLE", "")

#        buffer davy and join features within buffer
print "Running Buffer on Davy Trees..."
arcpy.Buffer_analysis(input_Davy, davy_buffer, "20 Feet", "FULL", "ROUND", "NONE")
print "Joining DPW Trees to Davy buffer..."
arcpy.SpatialJoin_analysis(input_DPW, davy_buffer, davyBuff_joinDPW)

#       Loop through records calculate match_prob
print "Calculating fields..."
rows = arcpy.UpdateCursor(davyBuff_joinDPW)
for row in rows:
   if row.AddressNo == row.Address:
      row.match_prob += 40
   if row.BOTANICAL.lower() == row.LatinName.lower() or row.CommonName.lower() == row.COMMON.lower():
      row.match_prob += 30
   if row.ICOUNT >= 2 or row.SiteOrder >= 2:
      row.match_prob += -5
   rows.updateRow(row)
   del row
del rows

print "***** CoincidentPoints Finished *****"