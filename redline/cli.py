# -*- coding: utf-8 -*- 
import argparse
import sys
if __name__ == "__main__":
    import tools
    import redmine
else:
    import tools as tools
    import redmine as redmine

def begin():
    parser = argparse.ArgumentParser(description='''Redline is Command Line Tools for REDMINE.\n
   ''')
    parser.add_argument('-v','--version',action='version',version='Redline 0.0.1')
    parser.add_argument('-sl','--shortline'
            ,action='store_true'
            ,dest='flag_shortline'
            ,help="Very short ticket output.")
    parser.add_argument('-d','--detail'
            ,action='store_true'
            ,dest='flag_detail'
            ,help="More Detail ticket output.")
    parser.add_argument('-cf','--configure'
            ,action='store'
            ,dest='configure_filename'
            ,type=str
            ,help='Read Other Configure File.')
    parser.add_argument('-s','--status_id'
            ,action='store'
            ,dest='status_id'
            ,type=str)
    parser.add_argument('-m','--assigned_to'
            ,action='store'
            ,dest='assigned_to'
            ,type=str)
    parser.add_argument('-p','--project_id'
            ,action='store'
            ,dest='project_id'
            ,type=str)
    parser.add_argument('-l',"--log"
            ,action="store"
            ,dest='log'
            ,type=str)
    parser.add_argument('-x',"--max"
            ,action="store"
            ,dest='limit'
            ,type=int)
    ### Sub Commands
    # -- init --
    subparsers = parser.add_subparsers(
            help='sub-commands')
    param_init = subparsers.add_parser(
            'init',
            help='When You use Redline first,do use option :) ')
    param_init.set_defaults(func=tools.initialize)
    # -- report --
    param_report = subparsers.add_parser('report'
            ,help="Daily Report Mode")
    param_report.add_argument('filepath'
            ,nargs='?'
            ,help="Daily Report Template File")
    param_report.set_defaults(func=daily_report)
    # -- close tickets
    param_close = subparsers.add_parser('close'
            ,help="Close Ticket (# + ticket_id)")
    param_close.add_argument('ticket',
            type=str)
    param_close.set_defaults(func=redmine.close)
    # -- done tickets
    param_done = subparsers.add_parser('done'
            ,help='Done Ticket')
    param_done.add_argument('ticket',
            type=str)
    param_done.add_argument('-r','--rate'
            ,action="store"
            ,dest='done_rate'
            ,help='Done Rate(0 - 100)')
    param_done.set_defaults(func=redmine.done)

    # -- assign tickets
    param_assign = subparsers.add_parser('assign'
            ,help="Assign Ticket")
    param_assign.add_argument('ticket',
            type=str)
    param_assign.set_defaults(func=redmine.assign)

    # -- show tickets (default) --
    param_show = subparsers.add_parser('show'
            ,help="Show tickets")
    param_show.set_defaults(func=show_tickets)

    # -- new tickets 
    param_new = subparsers.add_parser('new'
            ,help="new tickets")
    param_new.add_argument('-f','--file'
            ,action='store'
            ,dest='filepath'
            ,type=str)
    param_new.add_argument('-t','--template'
            ,action='store_true'
            ,dest='template_make')
    param_new.add_argument('-s','--subject'
            ,action='store'
            ,dest='subject_text'
            ,type=str)
    param_new.add_argument('-p','--project_id'
            ,action='store'
            ,dest='project_id'
            ,type=str)
    param_new.add_argument('-r','--priority'
            ,action='store'
            ,dest='priority_id'
            ,type=str)
    param_new.add_argument('-d','--description'
            ,action='store'
            ,dest='description'
            ,type=str)
    param_new.add_argument('-k','--tracker'
            ,action='store'
            ,dest='tracker_id'
            ,type=str)
    param_new.set_defaults(func=redmine.create)
    
    # -- project
    param_project = subparsers.add_parser('project'
            ,help="Show Project")
    param_project.add_argument('-d','--detail'
            ,action='store_true'
            ,dest='flag_detail')
    param_project.set_defaults(func=redmine.project_list)
    
    # -- me
    param_me = subparsers.add_parser('me'
            ,help="Your Id Details :)")
    param_me.set_defaults(func=redmine.your_detail)

    #try:
    if (len(sys.argv) < 2):
            cmd = parser.parse_args(["show"])
    elif not (
                "init"          in sys.argv
             or "report"        in sys.argv
             or "show"          in sys.argv
             or "create"        in sys.argv
             or "new"           in sys.argv
             or "close"         in sys.argv
             or "done"          in sys.argv
             or "new"           in sys.argv
             or "assign"        in sys.argv
             or "project"       in sys.argv
             or "me"            in sys.argv
             or "-h"            in sys.argv
             or "--help"        in sys.argv
             or "-v"            in sys.argv
             or "--version"     in sys.argv
             ):
            cmd = parser.parse_args(sys.argv[1:] + ["show"])
    else:
            cmd = parser.parse_args()
    #except:
    #    cmd = parser.parse_args(sys.argv[1:] + ["show"])

    opt = {
              'status_id':cmd.status_id
             ,'assigned_to_id':cmd.assigned_to
             ,'project_id':cmd.project_id
             ,'limit':str(cmd.limit)
          }

    cmd.func(cmd,opt)

def show_tickets(cmd,opt):
    print('''
   ____    U _____ u ____     _                  _   _   U _____ u 
U |  _"\ u \| ___"|/|  _"\   |"|        ___     | \ |"|  \| ___"|/ 
 \| |_) |/  |  _|" /| | | |U | | u     |_"_|   <|  \| |>  |  _|"   
  |  _ <    | |___ U| |_| |\\\\| |/__     | |    U| |\  |u  | |___   
  |_| \_\   |_____| |____/ u |_____|  U/| |\u   |_| \_|   |_____|  
  //   \\\\_  <<   >>  |||_    //  \\\\.-,_|___|_,-.||   \\\\,-.<<   >>  
 (__)  (__)(__) (__)(__)_)  (_")("_)\_)-' '-(_/ (_")  (_/(__) (__) 
            ''')
    conf = tools.load_configure(cmd.configure_filename)
    xml = redmine.load_redmine_xml(conf,opt)
    lines = dict_line(cmd,xml)
    for key,value in lines.items():
        print("---> " + key)
        for line in value:
            print(line)

def daily_report(cmd,opt):
    conf = tools.load_configure(cmd.configure_filename)
    xml  = redmine.load_redmine_xml(conf,opt)
    lines = dict_line(cmd,xml)
    if cmd.filepath is not None:
        report_string = redmine.build_daily_report(cmd.filepath,lines)
    else:
        report_string = redmine.build_daily_report(conf['TEMPLATE'],lines)
    print(report_string)

def dict_line(cmd,xml):
    return (redmine.line_issue_veryshort(xml) 
                    if cmd.flag_shortline else 
                    redmine.line_issue_detail(xml) if cmd.flag_detail else
                    redmine.line_issue_short(xml))

if __name__ == '__main__':
    begin()
