"""
doc.py - ReQL Module
Copyright 2013, Joe Doliner, joedoliner.com
"""
import json
import re
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def decamel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


commands = {}

docs = json.load(open("willie/modules/reql_docs.json"))
for section in docs["sections"]:
    for command in section["commands"]:
        for lang, value in command["langs"].iteritems():
            if "name" in value:
                commands[value["name"]] = command

def doc(willie, trigger):
    if trigger.group(2) == " " or trigger.group(2) == "" or str(trigger.group(2)) == None or str(trigger.group(2)) == "" or trigger.group(2) == None:
        willie.say("I'm sorry, " + str(trigger.nick) + ", but you must enter a command.")
        return

    try:
        doc_string = commands[trigger.group(2)]["description"]
        doc_string = doc_string.replace("\n", " ")
        doc_string = strip_tags(doc_string)
        willie.say(trigger.group(2) + ": " + doc_string)
    except:
        willie.say(trigger.group(2) + ": " + "Unrecognized command.")

doc.commands = ['doc']
doc.priority = 'medium'

if __name__ == '__main__':
    print __doc__.strip()
