
import csv
import re


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def corrected_names(data):
    name_list = []
    pattern = re.compile(r'^([а-яА-Я]+)[,|\s]([а-яА-Я]+)[,|\s]([а-яА-Я]+|)')
    # replace_names = r'\1, \2, \3'
    for people in data:
        people = ','.join(people)
        result = pattern.sub(r'\1, \2, \3', people).split(',')
        name_list.append(result)
    return name_list


def corrected_numbers(data):
    phone_list = []
    pattern = re.compile(r'(\+7|8)\s*\(?(\d{3})\)?(\s*|.)(\d{3})(\s*|.)(\d{2}).?(\d{2})\s*(\(?(доб\.)\s*(\d+)\)?)?')
    replace_numbers = r'+7(\2)\4-\6-\7 \9\10'
    for people in data:
        people = ','.join(people)
        result = pattern.sub(replace_numbers, people).split(',')
        phone_list.append(result)
    return phone_list


def delete_copies(data):
    contact_dict = {}
    for contacts in data:
        if contacts[0] in contact_dict:
            for item in range(len(contacts)):

                if contacts[item] and not data[contact_dict[contacts[0]]][item]:
                    data[contact_dict[contacts[0]]][item] = contacts[item]

                elif contacts[item] and data[contact_dict[contacts[0]]][item] != contacts[item]:
                    data[contact_dict[contacts[0]]][item + 1] = contacts[item]

            data.remove(contacts)
        else:
            contact_dict[contacts[0]] = data.index(contacts)

    return contacts_list


corrected_contacts_list = delete_copies(corrected_numbers(corrected_names(contacts_list)))


with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(corrected_contacts_list)
