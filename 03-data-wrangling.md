# Analytics-Engineer-assessment

###Summary

This script takes files from vendor1, vendor2, and vendor3 (the first two being local and the third through htttp request). It then combines these files into a the "all-users.csv" file, delivered to the working directory as specified by user. This file has the vendor ID, name, adress, email, phone number, date of birth, and registration dates of users accross all three vendors.


##Instructions
These instructions assume that you have some command line python package installer (such as pip) and python3.

1. Create a working directory folder with the files of vendor one and vendor 2, the "requirements.txt" and "datawrangling.py" from this repository.
2. Install packages in requirements.txt in command line.
  e.g.
``` bash
baseDir="<working directory>"
cd "${baseDir}"
pip install -r requirements.txt
```
3. In command line run python script with the working directory as an arguement
  e.g.
 ``` bash
baseDir="<working directory>"
python3 -u datawrangling.py "${baseDir}"
```

##To note about the output file:

The output file DOES NOT match users among different vendors so each line does not represent a unique user.
