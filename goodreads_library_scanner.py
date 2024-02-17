# Extracts data from a goodreads csv file to add to library.json.
##
import csv
import json

gr_file = open('goodreads_library_export.csv', newline='',encoding='utf8')
next(gr_file)   #skips first line
gr_lib = list(csv.reader(gr_file, delimiter=','))
gr_lib.reverse()

# 1: The script will scan and collect books marked as read.
# 2: The script will scan and collect books marked as unread
scan_for_read = int(input('Read? (0 or 1)'))

library_data = []

print('Scanning...')

for item in gr_lib:
    if int(item[22]) > 0:
        book_is_read = 1
    else: book_is_read = 0
    if scan_for_read != book_is_read:
        continue
    entry = {}
    entry['title'] = item[1]
    entry['attribution'] = item[2]
    entry['rating'] = int(item[7])
    entry['edition_notes'] = item[9]
    entry['comments'] = item[19]
    library_data.append(entry)

print('Writing...')

if scan_for_read == 0:
    with open('reading_list.json','w') as jsonfile:
        json.dump(library_data,jsonfile,indent=4)
else:
    with open('library.json','w') as jsonfile:
        json.dump(library_data,jsonfile,indent=4)

print('Done.')

# GOODREADS LIBRARY EXPORT CSV FILE
# ALL LINES:
# Book Id
# Title
# Author
# Author l-f
# Additional Authors
# ISBN
# ISBN13
# My Rating
# Average Rating
# Publisher
# Binding
# Number of Pages
# Year Published
# Original Publication Year
# Date Read
# Date Added
# Bookshelves
# Bookshelves with positions
# Exclusive Shelf
# My Review
# Spoiler
# Private Notes
# Read Count
# Owned Copies


#item[1] is title
#item[2] is author
#item[7] is rating
#item[9] is publisher
#item[14] is date read
#item[15] is date added
#item[16] is shelves
#item[18] is exclusive shelves
#item[19] is review
#item[22] is read count
