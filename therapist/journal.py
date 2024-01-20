import re

journal_regex_str = r"<GRATITUDE JOURNAL BEGIN>((.|\n)*)<GRATITUDE JOURNAL END>"

def extract_gratitude_journal(message: str):
    gratitude_entry = re.findall(journal_regex_str, message)[0]

    message = re.sub(journal_regex_str, "", message)

    # stub for storing into backend DB here?
    # with 

    return message

