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


def scan_for_email_or_phone(raw_string: str, pii_fault_set: set) -> None:
    """
        Scan string for telephone or email data. Append to fault list if True

        Args:
            raw_string - unedited input text to scan
            pii_fault_list - list to append to if there is pii data present

        Telephone patterns include (but not exclusive to):
        +447222555555
        +44 7222 555 555
        07222-555-555
        (0722) 5555555
        +44(0)7222 555 555
    """
    email_regex = "[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}"
    telephone_regex = "(\+?[0-9]?)?((.*?\d){10,14})"

    contains_email = re.findall(email_regex, raw_string)
    if len(contains_email) == 1:
        pii_fault_set.add('Email')
    elif len(contains_email) > 1:
        pii_fault_set.add('Emails')

    contains_telephone =  re.findall(telephone_regex, raw_string)
    if len(contains_telephone) == 1:
        pii_fault_set.add('Telephone Number')
    elif len(contains_telephone) > 1:
        pii_fault_set.add('Telephone Numbers')



def main():

    # create list for any pii data included in inputted string
    pii_fault_set = set()

    str_to_check = input("Please type your message you wish to ask a chat bot.")
    
    df_database = pd.read_csv('databases/customer.csv')

    # print(df_database)

    scan_for_email_or_phone(str_to_check, pii_fault_set)

    # pii columns from database excluding email and phone since checking above
    database_pii_cols = ['Title', 'FirstName', 'LastName', 'DateOfBirth', 
                         'Address1', 'Address2', 'City', 'PostCode']

    cleansed_list = cleanse_string(str_to_check)

    # loop over each row in database filtering to only pii columns
    for i, row in df_database[database_pii_cols].iterrows():
        # loop through each column in dataframe
        for col in database_pii_cols:
            data = str(row[col]).lower()
            print(f"Checking {col} column in database")
            # loop over each word to check
            for word in cleansed_list:
                print(f'checking for {word}')
                if word in data:
                    pii_fault_set.add(col)

    if len(pii_fault_set) > 0:
        raise Exception(f"""Your inputted text may contain the following pii data:
{', '.join(pii_fault_set)}
If this is the case please remove before sending to chatbot""")


if __name__ == '__main__':
    main()
