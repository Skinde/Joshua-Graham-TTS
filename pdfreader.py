from PyPDF2 import PdfReader
from TTS.api import TTS
from spellchecker import SpellChecker
from dehyphen import FlairScorer
import torch
import enchant


filename = "the-three-worlds-of-welfare-capitalism-1990.pdf"

pdf = PdfReader(filename)
text = ""

for page in pdf.pages[10:12]:
    text = text + page.extract_text()


temp = text.split()
spell = SpellChecker()



#Spell check PDF errors
i = 0
for i in range(len(temp)):
    corrected_word = temp[i]
    for c in temp[i]:
        if c == '~':
            corrected_word = spell.correction(temp[i])
    temp[i] = corrected_word


d = enchant.Dict("en_US")

#Remove Soft Hypens
i = 0
ln = len(temp) - 1
while i < ln:
    if temp[i].find('\xad') or temp[i].find('\u00ad') or temp[i].find('\N{SOFT HYPHEN}'):
        temp[i] = temp[i].replace('\xad', '')
        temp[i] = temp[i].replace('\u00ad', '')
        temp[i] = temp[i].replace('\N{SOFT HYPHEN}', '')
        if d.check(temp[i] + temp[i+1]):
            temp[i] = temp[i] + temp[i+1]
            temp.pop(i+1)
            ln -= 1
    i = i + 1

text = ""
for word in temp:
    text = text + word
    text = text + " "
text = text[:-1]

print(text)


device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
tts.tts_to_file(text=text, speaker_wav="joshua.wav", language="en", file_path="output.wav")



