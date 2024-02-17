# Command line app for maintaining a personal record of books (read, reading list, library, etc)
# but could in principle be used for any media.

import json

# Currently requires library.json to be in the same folder as MnemosyneCL.py
with open('library.json','r') as jsonfile:
    default_library = json.load(jsonfile)
    current_library = default_library


# Mainly for parsing abbreviations in the command line:
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
        field = fieldparser(field)
        self.info[field] = entry
        return self
    

def browse(field,query,source=current_library):
    # "Source" is the deserialized JSON library file.
    findings = []
    field = fieldparser(field)
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

def change_text_field(field,text):
    new_field = input(f'Enter {field}: ')
    # User can enter '>>' in command line for a pararaph break:
    new_field = line_break_parser(new_field)
    text.info[field] = new_field

def display_texts(list_of_texts):
    for number, text in enumerate(list_of_texts):
        print(f'[{number}]: {text}')

def open_text(text):
    for field, entry in text.info.items():
        if field == 'Edition Notes' or field == 'Comments':
            print(f'{field.capitalize()}:\n{entry}')
        else:
            print(f'{field.capitalize()}: {entry}')

def call_librarian(display=display_case):
    display_texts(display_case)
    userinput = input('Instructions: ')
    userinput = userinput.split()
    command = userinput[0]
    params = userinput[1:]

    # Search commands:
    # [field] [entry]
    if command in ['a','t']:
        search_term = ' '.join(params)
        try:
            display = browse(command,search_term)
        except:
            print('Error: Malformed query.')
        if len(display) == 0:
            print('Not found.')
    if command == 'r':
        rating = int(params[0])
        try:
            display = browse(command,rating)
        except:
            print('Error: Malformed query.')
        if len(display) > 0:
            display_texts(display)
        else:
            print('Not found.')

    # Edit commands:
    # rate [number] [rating]
    if command == 'rate':
        display_index = int(params[0])
        rating = int(params[1])
        try:
            display[display_index].edit('r',rating)
        except:
            print('Error: No such text.')
    # title [number]
    if command == 'title':
        display_index = int(params[0])
        try:
            change_text_field('Title',display[display_index])
        except:
            print('Error: No such text.')
    # attribution (or att) [number]
    if command == 'attribution':
        display_index = int(params[0])
        try:
            change_text_field('Attribution',display[display_index])
        except:
            print('Error: No such text.')
    # note [number]
    if command == 'note':
        display_index = int(params[0])
        try:
            change_text_field('Edition Notes',display[display_index])
        except:
            print('Error: No such text.')
    # comment [number]
    if command == 'comment':
        display_index = int(params[0])
        try:
            change_text_field('Comments',display[display_index])
        except:
            print('Error: No such text.')

    # Open commands
    # open [number]
    if command == 'open':
        display_index = int(params[0])
        try:
            open_text(display[display_index])
        except:
            print('Error: No such text.')

    if command == 'new':
        create_text()

    #if command == 'quit' or 'exit':
        #sys.exit()

    write(display)
    print('\n')

    return display


# Initialize:

while True:
    display_case = call_librarian(display_case)