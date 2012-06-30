
           ____    U _____ u ____     _                  _   _   U _____ u 
        U |  _"\ u \| ___"|/|  _"\   |"|        ___     | \ |"|  \| ___"|/ 
         \| |_) |/  |  _|" /| | | |U | | u     |_"_|   <|  \| |>  |  _|"   
          |  _ <    | |___ U| |_| |\\\\| |/__     | |    U| |\  |u  | |___   
          |_| \_\   |_____| |____/ u |_____|  U/| |\u   |_| \_|   |_____|  
          //   \\\\_  <<   >>  |||_    //  \\\\.-,_|___|_,-.||   \\\\,-.<<   >>  
         (__)  (__)(__) (__)(__)_)  (_")("_)\_)-' '-(_/ (_")  (_/(__) (__)

Redline
=======
Redline is Command Line for Redmine.

Install
=======

     git clone THIS_REPOSITORY
     sudo python setup.py install

Command
=======

      {me,show,project,init,done,new,report,close,assign}
                        sub-commands
       init                When You use Redline first,do use option :)
       report              Daily Report Mode
       close               Close Ticket (# + ticket_id)
       done                Done Ticket
       assign              Assign Ticket
       show                Show tickets
       new                 new tickets
       project             Show Project
       me                  Your Id Details :)

      optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -sl, --shortline      Very short ticket output.
      -d, --detail          More Detail ticket output.
      -cf CONFIGURE_FILENAME, --configure CONFIGURE_FILENAME
                            Read Other Configure File.
      -s STATUS_ID, --status_id STATUS_ID
      -m ASSIGNED_TO, --assigned_to ASSIGNED_TO
      -p PROJECT_ID, --project_id PROJECT_ID
      -l LOG, --log LOG
      -x LIMIT, --max LIMIT

