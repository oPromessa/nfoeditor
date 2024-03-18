# nfoeditor
Take a XLS database with NFO tags for your HomeVideo files and generate corresponding NFO files for your KODI Library.

## How to use
1. Edit example.xls to adjust.
2. Do not change 1st columne name: `url filename` points out to each of the NFO files to be edites
3. Following columnes on the 1st line of the XLS indicate the tags in the the NFO file to edit in the format `parent/child:type`type being `string` or `date`
4. Fill out each of the rows. Save the XLS
5. Run on the command line: `python nfolist.py example.xlsx`

## You need Python 3.x
* pandas: `pip install pandas`
