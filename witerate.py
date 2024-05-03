# Iterates through a Mnemosyne library so user can check each entry
# individually without manually going through JSON file.
# Currently only set up for wlist.json

import json
import Mnemosyne as mnem

def initialize_counter():
    try:
        with open('witercount.txt', 'r') as counterfile:            
            counter = counterfile.read()
            return int(counter)
    except:
        return 0

def save_count(i):
    with open('witercount.txt','w') as counterfile:
        counterfile.write(str(i))

def retrieve_text(index, library):
    text = mnem.Text()
    text.info = library.contents[index]
    return text

def delete_text(index, library):
    del library.contents[index]

def call_user(user_input,text,i,library):
    if user_input == 'nn':
        i+=1
    elif user_input == 'dd':
        delete_text(i,library)
    elif user_input in ('t','a','r','n','c'):
        field = mnem.fieldparser(user_input)
        mnem.change_text_field(text,field)
        # if field == 'Rating':
        #     text.info[field] = int(input('Enter {field}: '))
        # else:
        #     text.info[field] = input('Enter {field}: ')
    elif user_input == 'qq':
        return (False,i)
    else:
        print('Invalid input.')
    return (True,i)


if __name__ == '__main__':
    library = mnem.open_library('wlist')
    i = initialize_counter()

    running = True

    while running:
        text = retrieve_text(i, library)

        mnem.open_text(text)

        user_input = input('Instructions: ')
        status = call_user(user_input,text,i,library)
        running = status[0]
        i = status[1]

        library.commit()

    save_count(i)