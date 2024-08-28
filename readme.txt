1. Description

Mnemosyne is a command line utility for managing a database of books. It is intended to be used to create and update private reading logs, wishlists, personal library records, and the like, but can in principle be used for other purposes as well (for example, tracking a video game backlog).

The record format is intentionally minimal, and is not intended to track detailed data or metadata. (See Section 6 below for field info.)

Although Mnemosyne mainly uses the command line for its interface, it also uses the Tkinter GUI library to streamline editing certain fields and for creating new records.


2. Requirements
You must have Python 3 installed to use Mnemosyne.
You must also have Tkinter installed (run "pip install tk" if not).


2. Basic Use

In Linux, run Mnemosyne from the terminal with the following command:
python3 Mnemosyne.py
In Windows, double-click the Mnemosyne.py icon and a terminal session will open.

On launch, Mnemosyne will open the library file that is marked as default in config.json. (Libraries are also stored as JSON files in order to be human-readable.)

You will be prompted to give instructions to the librarian. See Section 5 below for a full list of commands. The most basic commands allow you to create new text records, edit or delete existing records, and search records in the currently open library by field. There are also commands for managing libraries (see Section 4).

You can only directly interact with records the librarian has retrieved and stored in the display. See Section 3 for more detail.

Although Mnemosyne is mainly a command line utility, it uses the TKinter GUI library to streamline editing certain fields and for creating new records.

To exit Mnemosyne, use "exit" or "quit."

Data is saved automatically whenever a record is created or modified.


3. The Display

The display is the list of texts or records that are currently in the hands of the librarian. New records are added to the display automatically. The "search" command returns results by overwriting the display, while "search+" appends the results to the end of the display.

Use the "display" command to print the titles currently in the display. Use the "open" command to print the contents of a record in the display. Use the "edit" command to edit its contents. Use the "del" command to delete a record from the library. See section 5 for details on all commands.


4. Libraries
Mnemosyne supports multiple library files. (For example, one for a reading log, another for a book wishlist.) Library information is storied in config.json.

If you are opening Mnemosyne for the first time, or if the config is otherwise blank, the program will prompt you to create a library. It will be marked as the default libarary automatically. If you have goodreads data to import, be sure to run goodreads_library_scanner.py first (see Section 7).

Once a library is created and defined as default, Mnemosyne will open it on launch. To open another library, use the "newlib" command. To switch the default library to whichever is currently open, use "switchdefault".

If for some reason 

If you are opening Mnemosyne for the first time, or if the config is otherwise blank, the program will prompt you to create a library. If you have goodreads data to import, be sure to run goodreads_library_scanner.py first (see Section 7).

To remove a library, library files and their associated config.json entries must be deleted manually through.


5. Commands

search [field abbreviation] [search term]
- Searches selected field in all records in the current library. The search term does not have to be a single word. Returns by overwriting the display.

search+ [field abbreviation] [search term]
- Same as search, except any records it retrieves are added to the existing display.

display
- Prints the list of titles currently in the display along with their indices.

open [display index]
- Prints all fields from a record.

edit [display index]
- Edit a record.

edit [display index] [field abbreviation]
- Edit a single field in a record.

new
- Create a new record.

del [display index]
- Deletes a record from the library.

openlib [library name]
- Open a library (must be defined in config.json).

newlib
- Create a new library and the first record in that library.

switchdefault
- Change the default library to whichever library is currently open.

help
- Reminds user to RTFM.

quit (or exit)
- Closes Mnemosyne.


6. Fields

Title
- The title of the book. Cannot be blank.

Attribution
- The author(s) of the book. Cannot be blank.

Rating
- The user's rating of the book. Must be an integer. If left blank it will default to 0, which represents a record with no rating. Other than that, the user is able to define their own rating system.

Edition Notes
- Metadata about the book (publisher, condition, etc), secondary author info (editors, translators), ownership status, etc.

Comments
- Thoughts and reviews, time and circumstances of reading, etc.

Field Abbreviations:
t = Title
a = Attribution
r = Rating
n = Edition Notes
c = Comments


7. Other Tools

The package includes two additional utilities in the form of Python scripts:

goodreads_library_scanner.py
- If you have downloaded your goodreads data as a CSV file, this script will convert it to Mnemosyne's JSON format. Run it the same way you would run Mnemosyne, making sure it and your goodreads data is in the same folder as Mnemosyne.py and config.json. The script will ask what your new library should be named, and whether you want to import read, to-read, or all books.

witerate.py
- A simple tool to iterate linearly, record by record, through a library file, for example to edit records that have been imported from the goodreads scanner.
