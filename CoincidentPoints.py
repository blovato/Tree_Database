#       COINCIDENT POINTS
#       Brenten Lovato
#       San Francisco,
#       Dept. of Public Works
#       6.30.15
#
#       USAGE: After geocoding there may be many overlapping points. This algorithm 
#              moves overlapping points in a specified direction at a specified 
#              distance. Also applies likelihood of locations accuracy from 0-100.

#       import and setup
print "***** RUNNING CoincidentPoints SCRIPT *****"
print "Importing Modules..."
import arcpy, sys
from arcpy import env
from math import sin, cos, radians, pi
env.overwriteOutput = 1

#       input variables and assign workspace
print "Setting Environment..."
input_ws = "C:\Users\blovato\Desktop\SFGISData_Brenten\PyTest"
input_fc = "Trees_June2015_sunset_join_collect_events.shp"
input_parcels = "Parcels_Zoning.shp"
input_streetDir = "streetsDir.shp"
distance = 10   # in feet
env.workspace = input_ws

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
#        join compass to point fc
if (not FieldExist(input_fc, "CompassA")):
   print "Joining 'CompassA' and 'DirMean' to the feature class..."
   arcpy.JoinField_management(input_fc, "CNN", input_streetDir, "CNN", ["CompassA","DirMean"])
if (not FieldExist(input_fc, "moved_X")):
   print "Adding 'moved_X' field..."
   arcpy.AddField_management(input_fc, "moved_X", "DOUBLE", "30", "30", "", "", "NULLABLE", "")
if (not FieldExist(input_fc, "moved_Y")):
   print "Adding 'moved_Y' field..."
   arcpy.AddField_management(input_fc, "moved_Y", "DOUBLE", "30", "30", "", "", "NULLABLE", "")

#       function to test if address number is even, returns true
def is_even(x):
   if x % 2 == 0:
      return True
   else:
      return False

#       function to calculate moved_X and moved_Y
def point_pos(x0, y0, d, theta, addressNum):
   if theta >= 45 and theta <= 135 or theta >= 225 and theta <= 315:
      if (not is_even(addressNum)):
         if theta >= 180:
            theta -= 180
         else:
            theta += 180
   else:
      if is_even(addressNum):
         if theta >= 180:
            theta -= 180
         else:
            theta += 180

   theta_rad = pi/2 - radians(theta)
   return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)

#       Loop through records and calculate moved_X and moved_Y
print "Calculating fields..."
rows = arcpy.UpdateCursor(input_fc)
for row in rows:
   #        If coincident point create new coords and save to 'moved_' fields
   if row.SiteOrder > 1:
      distance_move = distance * (row.SiteOrder - 1)
      newX_Y = point_pos(row.Xcoord, row.YCoord, distance_move, row.CompassA, row.AddressNo)
      #        assign new values to the field
      row.moved_X = float(newX_Y[0])
      row.moved_Y = float(newX_Y[1])
      rows.updateRow(row)
   #        if not coincident point copy previous coordinate to the 'moved_' fields
   else:
      row.moved_X = row.XCoord
      row.moved_Y = row.YCoord
      rows.updateRow(row)
   del row
del rows

print "***** CoincidentPoints Finished *****"