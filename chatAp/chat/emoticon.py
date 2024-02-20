import re
from emot.emo_unicode import UNICODE_EMOJI  # For emojis
from emot.emo_unicode import EMOTICONS_EMO  # For EMOTICONS


def contains_emojis(text):
    return any(c in UNICODE_EMOJI for c in text)

# Function for converting emojis into word
def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",", "").replace(":", "").split()))
    return text


# Function for converting emoticons into word
def convert_emoticons(text):
    for emot in EMOTICONS_EMO:
        #text = re.sub(r'\(' + emot + r'\)', "_".join(EMOTICONS_EMO[emot].replace(",", "").split()), text)
        text = text.replace(emot, EMOTICONS_EMO[emot])
    return text
#     for emot, replacement in EMOTICONS_EMO.items():
#         text = re.sub(re.escape(emot), replacement, text)
#     return text

# def convert_emoticons(text):
#     pattern = re.compile(r'(' + '|'.join(re.escape(emot) for emot in EMOTICONS_EMO) + r')')
#     return pattern.sub(lambda x: EMOTICONS_EMO[x.group()], text)

# # Emoji Convert
# text = "Hilarious 😂. The feeling of making a sale 😎, The feeling of actually fulfilling orders 😒"
# text_emoji = convert_emojis(text)
# print('TEXT EMOJI CONVERT')
# print(text_emoji)
#
# # # Emoticon Convert
# text = "Hello :-) :P :o :| :( :x"
# text_emoticon = convert_emoticons(text)
# print('TEXT EMOTICON CONVERT')
# print(text_emoticon)


