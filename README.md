# Bee_Project
For the Data Subscriber it will create a new data base and table if it does not already exist in the same directory
data being sent to it should be in this format --> (YY/MM/DD?HH/MM/SS?Temp?pres?Hum?illum?location) the ? is used as a seperator whilst processing the data string

for the api for the latest and most stable returns you want to use /bee_data/api/v4/data_base path as this is the latest version

for v4 only:

queries example ?condition=time>'12:20:22';location='London'&select=time:date
for conditions strings must have '' around them 
when multiple conditions are present use ; to seperate them
make sure to use the correct operator


for select they use : to seperate them
