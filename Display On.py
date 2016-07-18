import geomagic.app.v2
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()

print 'DISPLAY ON'
geo.set_option("Graphics/Disable Display", 0)