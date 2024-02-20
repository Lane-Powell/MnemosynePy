# Command line app for maintaining a personal record of books (read, reading list, library, etc)
# but could in principle be used for any media.

import json

def open_library(library_filename):
    with open(library_filename,'r') as jsonfile:
        library = json.load(jsonfile)
    return library

def set_default_library(library_name):
    filename = library_name+'.json'
    with open('default.text','w') as config:
        config.write(filename)

# Initialze: load library
try:
    with open('default.txt','r') as config:
        default_library = config.read()
except: print('Cannot find default.txt')
try:
    current_library = open_library(default_library)
except: print('Cannot find library defined in default.txt')


# Basic class for reading/writing records to/from library.json
# Class instance corresponds to a single record pulled from/to be written to library.json
class text:
    def __init__(self):
        # Index of entry in library.json
        # Defaults to -1 for new entries, which are appended to the end of the library with write()
        self.index = -1

        # Matches JSON library structure:
        self.info = {}

    def __repr__(self):
        return f'{self.info["Title"]} by {self.info["Attribution"]}'

    def edit(self,field,entry):
        self.info[field] = entry
        return self
    

def browse(field,query,source=current_library):
    # "Source" is the deserialized JSON library file.
    findings = []
    # Rating searches get special code because ints break the in keyword.
    if field == 'Rating':
        query = int(query)
        for (index, record) in enumerate(source):
            if query == record[field]:
                find = text()
                find.info = record
                find.index = index
                findings.append(find)
    # Code for all other searches:
    else:
        for (index, record) in enumerate(source):
            if query.lower() in record[field].lower():
                find = text()
                find.info = record
                find.index = index
                findings.append(find)
    return findings

def write(newrecords,library=current_library):
    # Takes a list of texts as inputs.
    for record in newrecords:
        # Adds new entry to end of JSON file if index is -1
        if record.index == -1:
            library.append(record.info)
        else:
            library[record.index] = record.info
    with open('library.json', 'w') as jsonfile:
        json.dump(current_library,jsonfile,indent=4)


# Command line interface stuff:
display_case = []

# For parsing abbreviations in the command line:
def fieldparser(abbreviation):
    field_parser_key = {
        't':'Title',
        'a':'Attribution',
        'n':'Edition Notes',
        'c':'Comments',
        'r':'Rating'
        }
    try:
        field = field_parser_key[abbreviation]
    except:
        field = abbreviation
    return field

def line_break_parser(string):
    # User can enter '>>' in command line for a pararaph break
    # Called by other functions
    string = string.replace('>>','\n\n')
    return string

def create_text(library=current_library):
    # Requires user input from command line
    newtext = text()
    newtext.info['Title'] = input('Enter title: ')
    newtext.info['Attribution'] = input('Enter attribution: ')
    newtext.info['Rating'] = int(input('Enter rating: '))
    newtext.info['Edition Notes'] = line_break_parser(input('Enter edition notes: '))
    newtext.info['Comments'] = line_break_parser(input('Enter comments: '))
    newrecord = [newtext]
    return write(newrecord,library)

def change_text_field(text,field):
    new_field_entry = input(f'Enter {field}: ')
    # User can enter '>>' in command line for a pararaph break:
    if field == 'Rating':
        new_field_entry = int(new_field_entry)
    # DELETE ONCE GUI IMPLEMENTED:
    if field in ('Edition Notes', 'Comments'):
        new_field_entry = line_break_parser(new_field_entry)
    text.info[field] = new_field_entry

def display_texts(list_of_texts):
    for number, text in enumerate(list_of_texts):
        print(f'[{number}]: {text}')

def open_text(text):
    for field, entry in text.info.items():
        if field == 'Edition Notes' or field == 'Comments':
            print(f'{field.capitalize()}:\n{entry}')
        else:
            print(f'{field.capitalize()}: {entry}')

def call_librarian(display,input):
    input = input.split()
    command = input[0]
    params = input[1:]

    # Search commands:
    # search [field] [terms]
    if command == 'search':
        field = fieldparser(params[0])
        search_terms = ' '.join(params[1:])
        try:
            display = browse(field,search_terms)
            if len(display) > 0:
                display_texts(display)
            else:
                print('Not found.')
        except:
            print('Error: Malformed query.')

    # Edit commands:
    # edit [display index] [field]
    elif command == 'edit':
        display_index = int(params[0])
        text_to_edit = display[display_index]
        field = params[1]
        field = fieldparser(field)
        try:
            change_text_field(text_to_edit,field)
            write([text_to_edit])
        except:
            print('Error: No such text.')

    # Open commands
    # open [display index]
    elif command == 'open':
        display_index = int(params[0])
        try:
            open_text(display[display_index])
        except:
            print('Error: No such text.')

    elif command == 'new':
        create_text()

    elif command == 'display':
        display_texts(display)

    return display


# Initialize: main loop
while True:
    print('\n')
    user_input = input('Instructions: ')
    print('\n')
    if user_input in ('quit','exit'):
        break
    display_case = call_librarian(display_case,user_input)