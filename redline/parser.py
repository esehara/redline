# -*- coding: UTF-8 -*-
import re

class Tickets:
    def __init__(self):
        self.parse_array = {
                  "subject": None
                 ,"project_id": None
                 ,"tracker_id": None
                 ,"priority_id": None
                 ,"description": None
                 }
        self.is_description = False
        self.temporary = "" 

    def done_description(self):
        self.is_description = False
        if self.temporary != "":
            self.temporary = self.temporary.rstrip()
            self.parse_array["description"] = self.temporary
            self.temporary = ""

def TicketParser(string):
    lines = string.split("\n")
    tickets = Tickets()

    for line in lines:
        if   re.search("^SUBJECT:",line) is not None:
            tickets.parse_array["subject"] = line.replace("SUBJECT:","")
            tickets.done_description()
        elif re.search("^PROJECT_ID:",line) is not None:
            tickets.parse_array["project_id"] = line.replace("PROJECT_ID:","").replace(" ","")
            tickets.done_description()
        elif re.search("^TRACKER_ID:",line) is not None:
            tickets.parse_array["tracker_id"] = line.replace("TRACKER_ID:","").replace(" ","")
            tickets.done_description()
        elif re.search("^PRIORITY",line) is not None:
            tickets.parse_array["priority_id"] = line.replace("PRIORITY:","").replace(" ","")
            tickets.done_description()
        elif re.search("^::DESCRIPTION::",line) is not None:
            tickets.is_description = True
        elif tickets.is_description:
            tickets.temporary += line + "\n"
    tickets.done_description()
    return tickets.parse_array

def TicketFile(file_object):
    return TicketParser(file_object.read())

def TicketTemplateOutput():
    print("""
SUBJECT: This is Subject id.
PROJECT_ID: This is Project id.
TRACKER_ID: This is Tracker id.
PRIORITY: This is PRIORITY.

::DESCRIPTION::

""")

if __name__ == "__main__":
    test_ticket = TicketParser("""
SUBJECT: これはテストのチケットです
PROJECT_ID: 1
TRACKER_ID: 2
PRIORITY: 4
::DESCRIPTION::
これはテストのチケットです
このチケットが通れば成功です。
""")
    for k,v in test_ticket.items():
        print(k + ":" + v)
