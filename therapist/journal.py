import regex

journal_regex_str = r"\/\*(.|\n)*\*\/"

def extract_gratitude_journal(message: str):
    regex.findall(journal_regex_str, message)

