# Extracts data from a goodreads csv file to add to library.json.

import csv
import json
from Mnemosyne import create_library


print('Goodreads library scanner for Mnemosyne (works as of August 2024)')
library_name = ' '
while ' ' in library_name or len(library_name.strip()) == 0:
    library_name = input('Enter the name of your new library (must be a valid filename, no spaces): ')

gr_file = open('goodreads_library_export.csv', newline='', encoding='utf8')
next(gr_file) # skips first line
gr_lib = list(csv.reader(gr_file, delimiter=','))
gr_lib.reverse()

print('Do you want to import read or unread books to your Mnemosyne library?')
scan_type = -1
while scan_type not in (0, 1, 2):
    scan_type = input('Enter 0 for unread, 1 for read, 2 for both:')
    try:
        scan_type = int(scan_type)
    except:
        scan_type = -1
if scan_type == 0:
    scan_for_read = 0
    scan_for_unread = 1
elif scan_type == 1:
    scan_for_read = 1
    scan_for_unread = 0
else:
    scan_for_read = 1
    scan_for_unread = 1

library_data = []

print('Scanning...')

for item in gr_lib:
    gr_readcount = int(item[22]) # Will be 0 if book is unread, 1 or more otherwise
    if int(item[22]) > 0:
        book_is_read = 1
        book_is_unread = 0
    else:
        book_is_read = 0
        book_is_unread = 1
    if (scan_for_unread != book_is_unread) and (scan_for_read != book_is_read):
        continue
    entry = {}
    entry['title'] = item[1]
    entry['attribution'] = item[2]
    entry['rating'] = int(item[7])
    entry['edition_notes'] = item[9]
    entry['comments'] = item[19]
    library_data.append(entry)

print('Writing...')

new_library = create_library(library_name)
new_library.contents.append(library_data)
new_library.commit()

print('Done.')

# GOODREADS LIBRARY EXPORT CSV FILE FORMAT
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
