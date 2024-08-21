# Command line app for maintaining a personal record of books (read, reading list, library, etc)
# but could in principle be used for any media.

import json


class Library:
    def __init__(self, name):
        self.name = name
        self.filename = name+'.json'
        self.contents = []

    def commit(self):
        with open(self.filename,'w') as jsonfile:
            json.dump(self.contents,jsonfile,indent=4)

# Called by call_librarian() when user attempts to open a library:
# Acts as a gate to block open_library from accepting invalid filenames
def check_valid_library(library_name):
# Check if library_name points to valid Mnemosyne library:
    with open('config.json','r') as config_file:
        config = json.load(config_file)
        for entry in config:
            if entry['name'] == library_name:
                return True
    return False

def open_library(library_name):
    library = Library(library_name)
    with open(library.filename,'r') as library_file:
        library.contents = json.load(library_file)
    return library
    
def set_default_library(library_name):
    with open('config.json','r') as config_file:
        config = json.load(config_file)
        for entry in config:
            if entry['name'] == library_name:
                entry['is_default'] = True
            else:
                entry['is_default'] = False
    with open('config.json','w') as config_file:
        json.dump(config,config_file,indent=4)


# Basic class for reading/writing records to/from library.json
# Instance corresponds to a single record pulled from/to be written to library.json
class Text:
    def __init__(self):
        # Index of entry in library.json
        # Defaults to -1 for new entries, which are appended to the end of the library with write_to_library()
        self.index = -1

        # Matches JSON library structure:
        self.info = {}

    def __repr__(self):
        return f'{self.info["Title"]} by {self.info["Attribution"]}'

    def edit(self, field, entry):
        self.info[field] = entry
        return self


def browse(field, query, source):
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

def write_to_library(new_record, library):
    if new_record.index == -1:
        library.contents.append(new_record.info)
    else:
        library.contents[new_record.index] = new_record.info


# Command line interface/GUI stuff:

import tkinter as tk

class InputWindow(tk.Tk):
    def __init__(self, existing_entry=''):
        super().__init__()
        self.title('Input Window')

        self.label = tk.Label(self, text='Enter your input:')
        self.label.pack()

        self.entry = tk.Text(self)
        self.entry.insert(tk.END, existing_entry)
        self.entry.pack()

        self.button = tk.Button(self, text='Done', command=self.save_input)
        self.button.pack()

    def save_input(self):
        self.new_field_entry = self.entry.get(1.0,'end').strip()
        # strip() to remove newline automatically added by tk.Text
        self.destroy()

class NewTextWindow(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)

        self.label = tk.Label(self, text='Enter new text info:')
        self.label.pack()

        self.text_title = tk.Entry(self)
        self.text_title.pack()

        self.attribution = tk.Entry(self)
        self.attribution.pack()

        self.rating = tk.Entry(self)
        self.rating.pack()

        self.edition_notes = tk.Text(self)
        self.edition_notes.pack()

        self.comments = tk.Text(self)
        self.comments.pack()

        self.button = tk.Button(self, text='Done', command=self.save_input)
        self.button.pack()

    def save_input(self):
        self.new_text_title = self.text_title.get()
        self.new_attribution = self.attribution.get()
        self.new_rating = self.rating.get()
        self.new_edition_notes = self.edition_notes.get(1.0,'end').strip()
        self.new_comments = self.comments.get(1.0,'end').strip()
        # strip() to remove newline automatically added by tk.Text
        self.destroy()

# Create an instance of the InputWindow class:
# input_window = InputWindow()
# input_window.mainloop()
# Access the user input after the window is closed:
# print("User input:", input_window.new_field_entry)

def create_library():
    # Requires user input from command line.
    new_library_name = ' '
    while ' ' in new_library_name or len(new_library_name) == 0:
        new_library_name = input('Enter library name (no spaces):')
    print('Now create the first entry in your new library.')
    first_entry = create_text()
    new_library = Library(new_library_name)
    new_library.contents.append(first_entry.info)
    # Creates JSON for new library:
    with open(new_library.filename,'w') as new_library_file:
        json.dump(new_library.contents,new_library_file,indent=4)
    # Adds library to config:
    with open('config.json','r') as config_file:
        config = json.load(config_file)
        config.append({'name':new_library_name,'is_default':False})
    with open('config.json','w') as config_file:
        json.dump(config,config_file,indent=4)
    # Returns name so it can be called by open_library:
    return new_library_name

# For parsing abbreviations in the command line:
def fieldparser(abbreviation):
    if abbreviation not in ('t','a','n','c','r'):
        raise ValueError('invalid field abbreviation')
    field_parser_key = {
        't':'Title',
        'a':'Attribution',
        'n':'Edition Notes',
        'c':'Comments',
        'r':'Rating'
        }
    field = field_parser_key[abbreviation]
    return field

def create_text():
    # Requires user input from command line.
    text = Text()

    new_text_window = NewTextWindow('New Entry')
    new_text_window.mainloop()
    text.info['Title'] = new_text_window.new_text_title
    text.info['Attribution'] = new_text_window.new_attribution
    text.info['Rating'] = int(new_text_window.new_rating)
    text.info['Edition Notes'] = new_text_window.new_edition_notes
    text.info['Comments'] = new_text_window.new_comments

    return text

def change_text_field(text, field):
    if field in ('Edition Notes','Comments'):
        input_window = InputWindow(text.info[field])
        input_window.mainloop()
        new_field_entry = input_window.new_field_entry
    else:
        new_field_entry = input(f'Enter {field}: ')
    if field == 'Rating':
        try:
            new_field_entry = int(new_field_entry)
        except ValueError:
            print('Error: Invalid parameter (rating must be an integer).')
    text.info[field] = new_field_entry
    return text

def change_all_text_fields(text):
    edit_text_window = NewTextWindow('Edit Entry')
    # Populate fields with current entries:
    edit_text_window.text_title.insert(tk.END,text.info['Title'])
    edit_text_window.attribution.insert(tk.END,text.info['Attribution'])
    edit_text_window.rating.insert(tk.END,text.info['Rating'])
    edit_text_window.edition_notes.insert(tk.END,text.info['Edition Notes'])
    edit_text_window.comments.insert(tk.END,text.info['Comments'])
    # Get new entries:
    edit_text_window.mainloop()
    text.info['Title'] = edit_text_window.new_text_title
    text.info['Attribution'] = edit_text_window.new_attribution
    text.info['Rating'] = int(edit_text_window.new_rating)
    text.info['Edition Notes'] = edit_text_window.new_edition_notes
    text.info['Comments'] = edit_text_window.new_comments
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

def call_librarian(display, current_library, input):
    input = input.split()
    command = input[0]
    params = input[1:]

    # print(len(params))
    
    if command in ('quit','exit'):
        return (False, display, current_library)

    # Search commands:
    # search [field] [terms]
    elif command == 'search':
        if len(params) == 0:
            print('Error: Missing parameter (field abbreviation).')
            print('Error: Missing parameter (search terms).')
            return (True, display, current_library)
        if len(params) == 1:
            print('Error: Missing parameter (search terms).')
            return (True, display, current_library)
        try:
            field = fieldparser(params[0])
        except ValueError:
            print('Error: Invalid parameter (field abbreviation).')
            return (True, display, current_library)
        search_terms = ' '.join(params[1:])
        display = browse(field, search_terms, current_library)
        if len(display) > 0:
            display_texts(display)
        else:
            print('Not found.')

    # Edit commands:
    # edit [display index] [field]
    elif command == 'edit':
        # Get text to edit:
        try:
            display_index = params[0]
        except IndexError:
            print('Error: Missing parameter (display index).')
            return (True, display, current_library)
        try:
            display_index = int(display_index)
        except ValueError:
            print('Error: Invalid parameter (display index).')
            return (True, display, current_library)
        try:
            text_to_edit = display[display_index]
        except IndexError:
            print('Error: No such text.')
            return (True, display, current_library)
        # Get field to edit if any and execute:
        if len(params) < 2:
            changed_text = change_all_text_fields(text_to_edit)
        else:
            try:
                field = params[1]
                field = fieldparser(field)
            except ValueError:
                print('Error: Invalid parameter (field abbreviation).')
                return (True, display, current_library)
            changed_text = change_text_field(text_to_edit,field)
        # Save edit:
        write_to_library(changed_text,current_library)
        display[display_index] = changed_text


    # Open commands:
    # open [display index]
    elif command == 'open':
        if len(params) == 0:
            print('Error: Missing parameter (display index).')
            return (True, display, current_library)
        try:
            display_index = int(params[0])
        except ValueError:
            print('Error: Invalid parameter (display index).')
            return (True, display, current_library)
        try:
            text_to_open = display[display_index]
        except IndexError:
            print('Error: No such text.')
            return (True, display, current_library)
        open_text(display[display_index])

    elif command == 'new':
        new_text = create_text()
        write_to_library(new_text, current_library)

    elif command == 'newlib':
        new_library = create_library()
        print('Ready to open.')

    elif command == 'switchdefault':
        set_default_library(current_library.name)
        print('Default library changed to current library.')

    # Open a library (and close current library):
    # openlib [library name]
    elif command == 'openlib':
        try:
            library_to_open = params[0]
        except IndexError:
            print('Required parameter: library name.')
            return (True, display, current_library)
        if check_valid_library(library_to_open):
            current_library = open_library(library_to_open)
            print(f'{library_to_open} is now open.')
        else:
            print('Invalid library name.')

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

    return (True, display, current_library)


if __name__ == '__main__':
    # Initialze: load default library
    try:
        with open('config.json','r') as config_file:
            config = json.load(config_file)
            for entry in config:
                if entry['is_default']:
                    default_library_name = entry['name']
    except FileNotFoundError: print('Cannot find config.json')
    try:
        current_library = open_library(default_library_name)
    except FileNotFoundError: print('Cannot find default library defined in config.json')

    status = True
    display = []

    # Main loop:
    while status == True:
        print('\n')
        user_input = input('Instructions: ')
        # Don't accept input if blank:
        if len(user_input) == 0 or user_input.isspace():
            continue
        print('\n')
        call = call_librarian(display, current_library, user_input)
        status = call[0]
        display = call[1]
        current_library = call[2]

    current_library.commit()