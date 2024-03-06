import string
import re

# requirements
from nltk.corpus import stopwords
import pandas as pd

# This is needed to download the stopwords resources
import nltk
nltk.download('stopwords')


def cleanse_string(raw_string: str) -> list:
    """
        Remove all stop words from string. (eg. a, is, the)
        Remove all duplicate words from string.

        Args:
            raw_string - unedited input text to scan

        Return:
            list of words to check for pii
    """
    
    cleansed_list = []
    
    # get all stopwords from nltk package
    stop_words = stopwords.words('english')

    # convert str to lowercase
    lower_string = raw_string.lower()

    # remove all punctuation from str
    lower_punc_string = lower_string.translate(str.maketrans('', '', string.punctuation))

    # loop over each word in str
    for word in lower_punc_string.split(' '):
        # check if word is a stop word or has returned empty str
        if word not in stop_words and word != '':
            # remove newline indicator from word
            cleansed_list.append(word.replace('\n', ''))

    # drop duplicate words from list by converting to set
    cleansed_set = set(cleansed_list)
    
    # convert set back to list
    cleansed_list = list(cleansed_set)

    return cleansed_list 


def scan_for_email_or_phone(raw_string: str) -> list:
    """
        Scan string for telephone or email data. Append to fault_list if True

        Args:
            raw_string - unedited input text to scan
            pii_fault_list - list to append to if there is pii data present
        
        Return: list containing if emails or telephone numbers are in the string
    """
    email_list = []
    phone_list = []
    fault_list = []

    word_list = raw_string.split(' ')

    email_regex = "^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}"
    telephone_regex = "^(\+?\d{1,3}?)([-.]?\d{1,3}){1,4}"

    # check each item in list is not an email
    for _word in word_list:
        contains_email = re.findall(email_regex, _word)
        print(contains_email)
        if len(contains_email) > 0:
            email_list.append('Email')
       
        # check each item in list is not a telephone numbers
        contains_telephone =  re.findall(telephone_regex, _word)
        if len(contains_telephone) > 0:
            phone_list.append('Telephone Number')

    # is plural needed?
    if len(email_list) > 1:
        fault_list.append('Emails')
    elif len(email_list) == 1:
        fault_list.append('Email')

    if len(phone_list) > 1:
        fault_list.append('Telephone Numbers')
    elif len(phone_list) == 1:
        fault_list.append('Telephone Number')

    return fault_list


def main():

    # create set for any pii data included in inputted string
    pii_fault_set = set()

    str_to_check = input("Please type your message you wish to ask a chat bot.")
    
    df_database = pd.read_csv('databases/customer.csv')

    # determine if email or phone number in str
    fault_list = scan_for_email_or_phone(str_to_check)
    pii_fault_set.update(fault_list)

    # pii columns from database excluding email and phone since checking above
    database_pii_cols = ['Title', 'FirstName', 'LastName', 'DateOfBirth', 
                         'Address1', 'Address2', 'City', 'PostCode']

    cleansed_list = cleanse_string(str_to_check)
    
    # loop through each possible pii column
    for col in database_pii_cols:
        print(f"Checking {col} column in database")
        # loop over each row in database filtering to only pii columns
        for i, row in df_database[database_pii_cols].iterrows():
            data = str(row[col]).lower()
            # loop over each word to check
            for word in cleansed_list:
                if word in data:
                    pii_fault_set.add(col)

    if len(pii_fault_set) > 0:
        print(f"""WARNING: Your inputted text may contain the following pii data:
{', '.join(pii_fault_set)}
If this is the case please remove before sending to chatbot""")


if __name__ == '__main__':
    main()
