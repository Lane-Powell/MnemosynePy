# Command line app for maintaining a personal record of books (read, reading list, library, etc)
# but could in principle be used for any media.

import json


class Library:
    def __init__(self,name,contents):
        self.name = name
        self.filename = name+'.json'
        self.contents = contents

    def commit(self):
        with open(self.filename, 'w') as jsonfile:
            json.dump(self.contents,jsonfile,indent=4)

def open_library(library_name):
    with open(library_name+'.json','r') as jsonfile:
        library_contents = json.load(jsonfile)
    library = Library(library_name,library_contents)
    return library
    
def set_default_library(library_name):
    filename = library_name+'.json'
    with open('default.txt','w') as config:
        config.write(filename)

# Initialze: load library
try:
    with open('default.txt','r') as config:
        default_library_name = config.read()
except: print('Cannot find default.txt')
try:
    current_library = open_library(default_library_name)
except: print('Cannot find library defined in default.txt')


# Basic class for reading/writing records to/from library.json
# Class instance corresponds to a single record pulled from/to be written to library.json
class Text:
    def __init__(self):
        # Index of entry in library.json
        # Defaults to -1 for new entries, which are appended to the end of the library with write_to_library()
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
        for (index, record) in enumerate(source.contents):
            if query == record[field]:
                find = Text()
                find.info = record
                find.index = index
                findings.append(find)
    # Code for all other searches:
    else:
        for (index, record) in enumerate(source.contents):
            if query.lower() in record[field].lower():
                find = Text()
                find.info = record
                find.index = index
                findings.append(find)
    return findings

def write_to_library(new_record,library=current_library):
    if new_record.index == -1:
        library.contents.append(new_record.info)
    else:
        library.contents[new_record.index] = new_record.info


# Command line interface/GUI stuff:
display_case = []

import tkinter as tk

class InputWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Input Window')

        self.label = tk.Label(self, text='Enter your input:')
        self.label.pack()

        self.entry = tk.Text(self)
        self.entry.pack()

        self.button = tk.Button(self, text='Done', command=self.save_input)
        self.button.pack()

    def save_input(self):
        self.new_field_entry = self.entry.get(1.0,'end')
        self.destroy()

# Create an instance of the InputWindow class
# input_window = InputWindow()
# input_window.mainloop()

# Access the user input after the window is closed
# print("User input:", input_window.new_field_entry)

# For parsing abbreviations in the command line:
def fieldparser(abbreviation):
    field_parser_key = {
        't':'Title',
        'a':'Attribution',
        'n':'Edition Notes',
        'c':'Comments',
        'r':'Rating'
        }
    field = field_parser_key[abbreviation]
    return field

def line_break_parser(string):
    # User can enter '>>' in command line for a pararaph break
    # Called by other functions
    string = string.replace('>>','\n\n')
    return string

def create_text():
    # Requires user input from command line
    text = Text()
    text.info['Title'] = input('Enter title: ')
    text.info['Attribution'] = input('Enter attribution: ')
    text.info['Rating'] = int(input('Enter rating: '))
    text.info['Edition Notes'] = line_break_parser(input('Enter edition notes: '))
    text.info['Comments'] = line_break_parser(input('Enter comments: '))
    return text

def change_text_field(text,field):
    if field in ('Edition Notes', 'Comments'):
        input_window = InputWindow()
        input_window.mainloop()
        new_field_entry = input_window.new_field_entry
        # DELETE ONCE GUI IMPLEMENTED:
        # User can enter '>>' in command line for a pararaph break:
        #new_field_entry = line_break_parser(new_field_entry)
    else:
        new_field_entry = input(f'Enter {field}: ')
    if field == 'Rating':
        new_field_entry = int(new_field_entry)
    text.info[field] = new_field_entry
    return text

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
        try:
            field = fieldparser(params[0])
        except:
            print('Error: Invalid parameter (field).')
            field = None
        search_terms = ' '.join(params[1:])
        if field is not None:
            display = browse(field,search_terms)
            if len(display) > 0:
                display_texts(display)
            else:
                print('Not found.')

    # Edit commands:
    # edit [display index] [field]
    elif command == 'edit':
        try:
            display_index = int(params[0])
            text_to_edit = display[display_index]
        except:
            print('Error: Invalid parameter (display index).')
            display_index = None
        try:
            field = params[1]
            field = fieldparser(field)
        except:
           print('Error: Invalid parameter (field).')
           field = None
        if field is not None and display_index is not None: 
            try:
                text_to_edit = display[display_index]
                changed_text = change_text_field(text_to_edit,field)
                write_to_library(changed_text)
                display[display_index] = changed_text
            except:
                print('Error: No such text.')

    # Open commands
    # open [display index]
    elif command == 'open':
        try:
            display_index = int(params[0])
        except:
            print('Error: Invalid parameter (display index).')
            display_index = None
        if display_index is not None:
            try:
                open_text(display[display_index])
            except:
                print('Error: No such text.')

    elif command == 'new':
        new_text = create_text()
        write_to_library(new_text)

    elif command == 'display':
        if len(display) > 0:
            display_texts(display)
        else:
            print('Nothing to display.')
    
    elif command == 'commit':
        current_library.commit()

    elif command == 'help':
        print('See readme.txt')

    else:
        print('Invalid command.')

    return display


# Initialize: main loop
while True:
    print('\n')
    user_input = input('Instructions: ')
    print('\n')
    if user_input in ('quit','exit'):
        break
    display_case = call_librarian(display_case,user_input)

current_library.commit()