# -*- coding: utf-8 -*-
import urllib
import os
import re
import xml.etree.cElementTree as etree

if __name__ == "__main__" or __name__ == "redmine":
    import tools
    import parser
else:
    import redline.tools as tools
    import redline.parser as parser

def isTicket(ticket):
    if re.search("^#([0-9]*)",ticket) is not None:
        return ticket.replace("#","")
    elif re.search("^([0-9]*)",ticket) is not None:
        return ticket
    else:
        print("Oops!! :( '" + ticket + "' is Not Ticket. ex.'#0000' ")
        exit()

def __prexml(xml):
    return '''<?xml version="1.0"?>
    <issue>
        %s
    </issue>
''' %(xml)

def ticket_url(cmd):
    conf = tools.load_configure(cmd.configure_filename)
    return conf["URL"] + ("issues/%s.xml?key=%s" %(isTicket(cmd.ticket),conf["API_KEY"]))

def create_xml(subject,project_id,priority=None,description=None,tracker_id=None):
    
    if priority is None:
        priority_xml = ""
    else:
        priority_xml = "<priority_id>%s</priority_id>" %(priority) 
    
    description_xml = "<description>%s</description>" %(description)
    
    if tracker_id is None:
        tracker_xml = ""
    else:
        tracker_xml = "<tracker_id>%s</tracker_id>" %(tracker_id)
    
    return __prexml('''    <subject>%s</subject>
    <project_id>%s</project_id>
    %s
    %s
    %s
''' %(subject,project_id,tracker_xml,priority_xml,description_xml))

def create(cmd,opt):
    import urllib
    conf = tools.load_configure(cmd.configure_filename) 
    if cmd.make_template:
        parser.TicketTemplateOutput() 
        exit()
    if cmd.filepath is not None:
        file_result = parser.TicketFile(open(cmd.filepath))
        cmd.subject_text = file_result["subject"]
        cmd.project_id    = file_result["project_id"]
        cmd.tracker_id    = file_result["tracker_id"]
        cmd.priority_id   = file_result["priority_id"]
        cmd.description   = file_result["description"]
    if (cmd.subject_text is None
       or cmd.project_id is None):
        print("Oops !! Subject and Project_id is not found :(")
        exit()
    xml = create_xml(cmd.subject_text,cmd.project_id,cmd.priority_id,cmd.description,cmd.tracker_id)
    print("Post xml now :)")
    print(xml)
    tools.post(conf["URL"] + "issues.xml?key=" + conf["API_KEY"],xml)
    print("create Issue :)")

def your_detail(cmd,opt):
    conf = tools.load_configure(cmd.configure_filename)
    xml_data_path = conf["URL"] + "users/current.xml?key=" + conf["API_KEY"]
    xml = etree.parse(urllib.urlopen(xml_data_path))
    print("\n\nHi!! Mr.%s :)" %(xml.find(".//firstname").text))
    print("Redmine URL is " + conf["URL"])
    print("Your Redmine Id is " + xml.find(".//id").text)
    print("\n\n")

def project_list(cmd,opt):
    conf = tools.load_configure(cmd.configure_filename)
    xml_data_path = conf["URL"] + "projects.xml?key=" + conf["API_KEY"]
    xml = etree.parse(urllib.urlopen(xml_data_path)).findall('.//project')
    for x in xml:
        print("[" + x.find("./id").text + "]" + x.find("./name").text)
        if cmd.flag_detail:
            print("--------------------")
            print(x.find("./description").text)
            print("\n")
    
def assign(cmd,opt):
    conf = tools.load_configure(cmd.configure_filename)
    if not "REDMINE_ID" in conf:
        xml_data_path = conf["URL"] + "users/current.xml?key=" + conf["API_KEY"]
        xml = etree.parse(urllib.urlopen(xml_data_path)).find('.//id')
        print("""Oops!! :(
Your Redmine Id is not found by Configure Yaml.

your_home_dir/.redline
-> REDMINE_ID: 666

oh,don't you know your redmine id ?
your redmine id is %s :) Have a fun!!
""" %(xml.text))
        exit()
    xml = __prexml('<assigned_to_id>%i</assigned_to_id>' % (conf["REDMINE_ID"]))
    tools.put(ticket_url(cmd),xml)
    print('ticket %s is Assigned by you.' % (cmd.ticket))

def done(cmd,opt):
    if cmd.done_rate is None:
        done_ratio = '100'
    else:
        done_ratio = cmd.done_rate
    
    if int(done_ratio) == 0:
        status = '1'
    elif int(done_ratio) > 0 and int(done_ratio) < 100:
        status = '2'
    elif int(done_ratio) == 100:
        status = '3'
    
    xml = __prexml('''<done_ratio>%s</done_ratio>
    <status_id>%s</status_id>''' %(done_ratio,status) )
    tools.put(ticket_url(cmd),xml)
    print('ticket %s is change -> done rate is %s' % (cmd.ticket,done_ratio))

def close(cmd,opt):
    xml = __prexml('<status_id>%s</status_id><notes>%s</notes>' %(5,cmd.log))
    tools.put(ticket_url(cmd),xml)
    print('ticket %s is close' %(cmd.ticket))    

def build_daily_report(filepath,dict_array=None):
    import datetime
    import re 
    if not os.path.isfile(filepath):
        print("Oops!! That file is not exist :(")
    template = open(filepath).read()
    today_match = re.search("\!{Today=(.*)}",template)
    if today_match is not None:
        d = datetime.datetime.today()
        template = template.replace("!{Today=" + today_match.group(1) + "}",today_match.group(1) % (d.year,d.month,d.day))
    tickets = re.search("\!{Tickets}",template)
    line_array = []
    if tickets is not None and dict_array is not None:
        for key,value in dict_array.items():
            line_array.append("\n" + key + u"\n----")
            for j in value:
                line_array.append(j)
        replace_string = "\n".join(line_array).encode("UTF-8")
        template = template.replace("!{Tickets}",replace_string)
    return template
        

def build_param(opt):
    param = ""
    if opt is None:
        return param
    for key,value in opt.items():
        if value is not None:
            param += key + "=" + value + "&"
    return param

def build_xmlpath(configure,url_opt):
    if "API_KEY" in configure:
        xml_data_path = configure["URL"] + "issues.xml?key=" + configure["API_KEY"] + "&" + url_opt 
    else:
        xml_data_path = configure["URL"] + "issues.xml?" + url_opt
    return xml_data_path

def load_redmine_xml(configure,opt=None):
    url_opt = build_param(opt)
    xml_data_path = build_xmlpath(configure,url_opt)
    xml_data = urllib.urlopen(xml_data_path)
    if __name__ == "__main__":
        print(urllib.urlopen(xml_data_path).read())
    return etree.parse(xml_data)

def line_issue_veryshort(issue_tree):
    lines_issue = {}
    for i in issue_tree.findall('./issue'):
        if not i.find('./project').get('name') in lines_issue:
            lines_issue[i.find('./project').get("name")] = []
        lines_issue[i.find('./project').get("name")].append("* #" + i.find('./id').text + " " + i.find('./subject').text + " " + i.find('./done_ratio').text + u"%完了")
    return lines_issue 

def line_issue_short(issue_tree):
    lines_issue = {}
    for i in issue_tree.findall('./issue'):
        elem = i.find('./project')
        if not elem.get("name") in lines_issue:
            lines_issue[elem.get("name")] = []
        lines_issue[elem.get("name")].append("* #" + i.find('./id').text + " [" + i.find("./status").get("name") + "][" + i.find('./priority').get("name") + "]" + "[" + i.find('tracker').get('name') + "] " + i.find('./done_ratio').text + "% "  + i.find('./subject').text + (" by " + i.find("./assigned_to").get("name") if i.find('./assigned_to') is not None else "" ))
    return lines_issue

def line_issue_detail(issure_tree):
    lines_issue = {}
    for i in issure_tree.findall('./issue'):
        elem = i.find('./project')
        dict_name = "ID:" + elem.get("id") + ",Name:" + elem.get("name")
        if not dict_name in lines_issue:
            lines_issue[dict_name] = []
        lines_issue[dict_name].append("* #" + i.find('./id').text + " [" + i.find("./status").get("name") + "][" + i.find('./priority').get("name") + "]" + "[" + i.find('tracker').get('name') + "] " + i.find('./done_ratio').text + "%"  + i.find('./subject').text + "\n=============\n\n" + (i.find('./description').text if i.find('./description').text is not None else "" ) + "\n\n")
    return lines_issue

if __name__ == "__main__":
    import tools
    conf = tools.load_configure()
    xml = load_redmine_xml(conf,None)
    lines = line_issue_short(xml)
    for key,value in lines.items():
        print("---> " + key)
        for line in value:
            print(line)

