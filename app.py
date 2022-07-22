from flask import Flask, render_template, request
from flask.wrappers import Response
import git
#import requests
import pprint
import csv
import pandas as pd
#from tkinter import *
#from tkinter.filedialog import askopenfilename
import tempfile #STORE FILES
import smtplib #EMAIL
from email.message import EmailMessage #EMAIL
import json	 #API
import urllib
import static.functions


#from io import StringIO

app = Flask(__name__)

scroll=False


#CODE WILL PULL FROM GITHUB and check for updates to github code
@app.route('/git_update', methods=['POST'])
def git_update():
 repo = git.Repo('./CSV-Checker-Web-Program')
 origin = repo.remotes.origin
 repo.create_head('main', 
 origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
 origin.pull() 
 return '', 200


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        results = []
        results2 = []
        output = []
        output_email = []
        highlight = []

        tempfile_path = "none"
        file = "none"
        extended_path = ""
        
        # IF Url = "http://127.0.0.1"#"https://"
        # All this is so that the example files work
        http_host = "" 
        path_info = request.url 
        print("http_host: " + http_host)
        print("path_info: " + path_info)
        if(path_info ==  "http://127.0.0.1:5000/"):
          print("LOCAL? YES")
        else:
          print("LOCAL? NO")
          extended_path = "/home/CSVchecker/CSV-Checker-Web-Program/static/"



  #////////////////////////////////////////////////////////////////////////////////////
  #
  #   SAMPLE TEXT:
  #
  #IP Address,Port,Code,Country,Anonymity,Google,Https,Last Checked
  #188.166.83.17,3128,NL,Netherlands,anonymous,no,no,2 seconds ago
  #193.70.96.193,80,FR,France,anonymous,no,no,2 seconds ago
  #187.17.145.237,30279,BR,Brazil,elite proxy,no,yes,2 seconds ago
  #191.96.42.80,3128,US,United States,anonymous,no,no,2 seconds ago
  #88.198.24.108,8080,DE,Germany,anonymous,no,no,2 seconds ago
  #194.182.87.125,8080,CZ,Czech Republic,anonymous,no,no,2 seconds ago
  #80.188.239.106,39271,CZ,Czech Republic,elite proxy,no,no,2 seconds ago
  #167.71.171.243,80,US,United States,elite proxy,no,no,2 seconds ago
  #95.85.36.236,8080,NL,Netherlands,anonymous,no,no,2 seconds ago
  #200.89.178.182,80,AR,Argentina,anonymous,no,no,2 seconds ago
  #179.108.169.71,8080,BR,Brazil,elite proxy,no,yes,2 seconds ago
  #175.28.14.2,80,MY,Malaysia,anonymous,no,no,2 seconds ago
  #103.106.119.154,8080,BD,Bangladesh,elite proxy,no,yes,2 seconds ago
  #36.89.8.234,8080,ID,Indonesia,elite proxy,no,no,2 seconds ago
  #110.74.221.18,53348,KH,Cambodia,elite proxy,no,yes,2 seconds ago
  #58.152.48.166,80,HK,Hong Kong,anonymous,no,no,2 seconds ago
  #
  #
  #///////////////////////////////////////////////////////////////////////////////////
        
        #FEEDBACK:
        feedback_name = request.form.get('nameF')
        feedback_email = request.form.get('emailF')
        feedback_message = request.form.get('messageF')
        
        print('\n\n Feedback \n\n')
        print('-'+str(feedback_name)+'-')

        
        '''
        if ((str(feedback_name) != "") and (str(feedback_name) != "None")):
          print("Feedback- NOT blank")
        else:
          print("Feedback- blank")
        '''

        

        #Gets the TEXTBOX variable from textarea then based on if there is file or not it will proceed slitly differently
        user_csv_userinput = request.form.get('user_csv')
        
        #determining which example to use: working or non-working
        example = request.form.get('upload_working')
        
        #CSV Type:
        csv_type = request.form.get('csv_type')
          
        #Values: Addresses_Geofences, tags_and_attributes, Fuel, Assets, Routes, Users, Drivers  
        
        
        #FEEDBACK FIRST CHECK
        
        if ((str(feedback_name) != "None")): #for some reason default value is none, not blank.. (str(feedback_name) != "")
          df_data_vojta = ""


          #EMAIL STUFF
          #////////////////////////////////////////////////////////////////////////////////////

          body1 = feedback_message
          #body = ('Input:\n\n', df_data,'- Output:\n\n', output)
        
          EmailAdd = "vojtaripa@gmail.com" #senders Gmail id over here
          Pass = "rnlnndgxawzdrejh" #senders Gmail's Password over here 

          msg = EmailMessage()
          msg['Subject'] = ('FEEDBACK - CSV Checker Results - '+feedback_name) # Subject of Email
          msg['From'] = EmailAdd
          msg['To'] = ['vojtaripa@gmail.com', 'vojta.ripa@samsara.com',feedback_email] # Reciver of the Mail
          msg.set_content(body1) # Email body or Content

          #### >> Code from here will send the message << ####
          try:
              with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: #Added Gmails SMTP Server
                  smtp.login(EmailAdd,Pass) #This command Login SMTP Library using your GMAIL
                  smtp.send_message(msg) #This Sends the message
              print ('Email sent successfully!')

          except:
              print ('OH NO! Something went wrong...')

          #Redirects page:   
          return render_template('data.html', df2=feedback_name)
        
        #//////////////////////////////////////////////////////////
        #WORKING EXAMPLE
        #//////////////////////////////////////////////////////////
        elif (user_csv_userinput == "" and example == "working"):
          # Input file
          
          # <FileStorage: 'FINAL_non_working_example.csv' ('text/csv')>
          file = extended_path + 'FINAL_working_example.csv'
          tempfile_path = 'FINAL_working_example.csv'
          
          #tempfile_path = tempfile.NamedTemporaryFile().name
          #file.save(tempfile_path)

          # Put input file in dataframe
          df = pd.read_csv(extended_path + 'FINAL_working_example.csv') #, na_filter=False) #, encoding='cp1252'
          df_no_Nan = pd.read_csv(tempfile_path, na_filter=False) #, encoding='cp1252'

          df2 = df.rename(str.lower, axis='columns')
          df2_no_Nan = df_no_Nan.rename(str.lower, axis='columns')

          df_data_vojta = pd.DataFrame(df2)

          
          #NOW TO MAKE TABLE ON NEXT PAGE:
          table_data = df2_no_Nan #sheet
          reader = csv.DictReader(table_data)
          
          
          for row in reader:
              results.append(dict(row))

          fieldnames = [key for key in results[0].keys()]

        #//////////////////////////////////////////////////////////
        #NON-WORKING EXAMPLE
        #//////////////////////////////////////////////////////////
        elif (user_csv_userinput == "" and example == "non-working"):
          # Input file
          
          # <FileStorage: 'FINAL_non_working_example.csv' ('text/csv')>
          file = extended_path + 'FINAL_non_working_example.csv'
          tempfile_path = 'FINAL_non_working_example.csv'

          # Put input file in dataframe
          df = pd.read_csv(extended_path + 'FINAL_non_working_example.csv') #, na_filter=False) #, encoding='cp1252'
          df_no_Nan = pd.read_csv(tempfile_path, na_filter=False) #, encoding='cp1252'

          df2 = df.rename(str.lower, axis='columns')
          df2_no_Nan = df_no_Nan.rename(str.lower, axis='columns')

          df_data_vojta = pd.DataFrame(df2)

          
          #NOW TO MAKE TABLE ON NEXT PAGE:
          table_data = df2_no_Nan #sheet
          reader = csv.DictReader(table_data)

          for row in reader:
              results.append(dict(row))

          fieldnames = [key for key in results[0].keys()]

        
        #//////////////////////////////////////////////////////////
        #executing FILE UPLOAD (Doesnt Quite work with some files)
        #//////////////////////////////////////////////////////////
        elif user_csv_userinput == "":
        

  # HERE IS WORKING CODE THAT WILL CREATE HTML TABLE / ARRAY:
          '''
          user_csv_userinput = request.form.get('user_csv')

          #WORKING used to create table on HTML page:
          user_csv = request.form.get('user_csv').split('\n')

          reader = csv.DictReader(user_csv)

          for row in reader:
              results.append(dict(row))

          fieldnames = [key for key in results[0].keys()]
          '''
          #user_csv_userinput = ""
          #fieldnames         = ""
          #results            = 'IP Address,Port,Code,Country,Anonymity,Google,Https,Last Checked\n188.166.83.17,3128,NL,Netherlands,anonymous,no,no,2 seconds ago'


          # Input file
          file = request.files['input_file']
          if not file:
              return "No file"

          tempfile_path = tempfile.NamedTemporaryFile().name
          file.save(tempfile_path)

          '''
          FROM SCOTTS WORKING PROGRAM:

          df = pd.read_csv(filename)
          df2 = df.rename(str.lower, axis='columns')
          df_data = pd.DataFrame(df2) 
          '''
          

          # Put input file in dataframe
          df = pd.read_csv(tempfile_path) #, na_filter=False) #, encoding='cp1252'
          df_no_Nan = pd.read_csv(tempfile_path, na_filter=False) #, encoding='cp1252'

          df2 = df.rename(str.lower, axis='columns')
          df2_no_Nan = df_no_Nan.rename(str.lower, axis='columns')

          df_data_vojta = pd.DataFrame(df2)
          
          #check if file bigger than 500 lines.. 
          if(len(df_data_vojta)>500 ):
            myerror = "File bigger than 500 lines. Please reduce file to 500 entries."
            return render_template('home.html', error=myerror)

          
          #NOW TO MAKE TABLE ON NEXT PAGE:
          table_data = df2_no_Nan #sheet
          reader = csv.DictReader(table_data)

          for row in reader:
              results.append(dict(row))

          fieldnames = [key for key in results[0].keys()]

        


        #//////////////////////////////////////////////////////////
        #IF uploading from textbox directly (WORKS)
        #//////////////////////////////////////////////////////////
        else:
          df ={}
          df2=pd.DataFrame(df)
          df2_no_Nan = {}
          #user_csv_userinput = request.form.get('user_csv')

          #WORKING used to create table on HTML page:
          user_csv = request.form.get('user_csv').split('\n')

          reader = csv.DictReader(user_csv)

          for row in reader:
              results.append(dict(row))

          fieldnames = [key for key in results[0].keys()]

        #return render_template('data.html', data=df_data_vojta)

        #//////////////////////////////////////////////////////////

        #This is the text based csv information:
        
          df = request.form.get('user_csv').split('\n')

          reader = csv.DictReader(df)
          for row2 in reader:
              print('\t'.join(row2))
              results2.append(dict(row2))

          #result will be here:
          df_data_vojta = pd.DataFrame(results2) #results2 #df4


          #needed to adjust my headers to be lower case so that it would work with rest of the code!
          #Previous Scotts code had this which did the same thing: df2 = df.rename(str.lower, axis='columns')
          df_data_vojta.columns= df_data_vojta.columns.str.lower()
        

#//////////////////////////////////////////////////////////
# NOW FINISH REST OF THE CODE: (all variables from above should be the same now)
#//////////////////////////////////////////////////////////

        print("DF_DATA from VOJTAS PROGRAM:\n\n")
        
        #print(df_data_vojta)
        df_data = df_data_vojta


#////////////////////////////////////////////////////////////////////////////////////
        
        

        #******************************************************************************************************************************************
        # Code will have to go below this line from Scott
        # massaging the data, running it through functions and getting results
        # Make sure to INDENT properly!
        #******************************************************************************************************************************************



        #now located in static/functions.py FILE




#******************************************************************************************************************************************
# Now returning output to HTML and sending it to page: home.html:
#******************************************************************************************************************************************
        '''
        print("blank_licensenumber results: \n")
        blank_licensenumber = remove_blank_driver(create_driver_list(df_data_vojta))
        blank_licensenumber = str(blank_licensenumber) + " HI "
        '''

        #executing all functions above (checkers) converting them to string and assigning results to strings, then displaying one long string in all_results which gets set to HTML text box
        '''
        driver_check        = driver_check(remove_blank_driver(create_driver_list(df_data)))
        username_check      = username_check(remove_blank_user(create_user_list(df_data)))
        blank_licensenumber = blank_licensenumber(df_data)
        blank_licensestate  = blank_licensestate(df_data)
        ruleset             = ruleset(df_data)
        invalid_header      = invalid_header(df_data)

        all_results= "\ndriver check: \n" + driver_check + "\nusername check: \n" + username_check  + "\nblank license number:" + "\nblank license state: \n" + blank_licensestate + "\nruleset:\n" + ruleset + "\ninvalid header:\n" + invalid_header
         '''
        #df2 = df_data_vojta.to_dict()

        ##########################################################################
        # NOW ADDING RESULTS TO ARRAY to be displayed on next HTML page:
        ##########################################################################

        #1. Potential Issues with your Driver Set Up:
        output.append('1. Potential Issues with your Driver Set Up: Driver Check')
        driver_check        = static.functions.driver_check(static.functions.remove_blank_driver(static.functions.create_driver_list(df_data_vojta,output,highlight),output,highlight),output, highlight)
        output.append('1. Potential Issues with your Driver Set Up: Username Check')
        username_check      = static.functions.username_check(static.functions.remove_blank_user(static.functions.create_user_list(df_data_vojta,output,highlight),output,highlight),output,highlight)


        #2. Potential Issues with your License Plate Numbers or States
        output.append('2. Potential Issues with your License Plate Numbers or States:')
        blank_licensenumber = static.functions.blank_licensenumber(df_data_vojta, df_data, output, highlight)
        #NO LONG USED?  = static.functions.blank_licensestate(df_data_vojta, df_data, output, highlight)


        #3. Potential Issues with your Driver Rulesets
        output.append('3. Potential Issues with your Driver Rulesets:')
        ruleset             = static.functions.ruleset(df_data_vojta, output, highlight)


        #4. Potential Issues with your CSV Headers
        output.append('4. Potential Issues with your CSV Headers:')
        invalid_header      = static.functions.invalid_header(df_data_vojta, output, highlight)
        
        #NEW
        output.append('5. Potential Issues with your Time Zones:')
        static.functions.timezone_check(df_data_vojta,output,highlight)
        
        output.append('6. Potential Issues with your ELD Day Start Times:') 
        static.functions.start_time(df_data,highlight, output)
        
        output.append('7. Potential Issues with your Driver Statuses:')
        static.functions.driverstatus(df_data, output, highlight)
        

        print("Object type: \n")
        print(df_data_vojta)
        print("\n \n")


        #print("value of output: " + output)
        pretty_output = pprint.pprint(output)

        #size is how many errors I have, Ignooring the 4 titles / functions I'm running
        size = (len(output)-8)  #If new functions need to add header here... 

        #EMAIL STUFF
        #////////////////////////////////////////////////////////////////////////////////////
        info1 = df_data.to_string()
        info2 = "\n".join(output)
        info3 = "<br>".join(output)
        myfile= str(file)
        body1 = 'File: '+myfile+'Filepath\n' + str(tempfile_path) + '\n\nOG Data:\n\n'+str(df)+ '\n\nTable:\n\n'+str(df2.to_html())+'\n\nInput:\n\n' + info1 + '\n\nOutput:\n\n'+ info2
        #body = ('Input:\n\n', df_data,'- Output:\n\n', output)
        
        EmailAdd = "vojtaripa@gmail.com" #senders Gmail id over here
        Pass = "rnlnndgxawzdrejh" #senders Gmail's Password over here 

        msg = EmailMessage()
        msg['Subject'] = ('CSV Checker Results - '+myfile) # Subject of Email
        msg['From'] = EmailAdd
        msg['To'] = ['vojtaripa@gmail.com', 'vojta.ripa@samsara.com', 'scott.roan@samsara.com'] # Reciver of the Mail
        msg.set_content(body1) # Email body or Content

        msg.add_alternative("""\
        <!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Simple Transactional Email</title>
    <style>
      /* -------------------------------------
          GLOBAL RESETS
      ------------------------------------- */
      
      /*All the styling goes here*/
      
      img {
        border: none;
        -ms-interpolation-mode: bicubic;
        max-width: 100%; 
      }

      body {
        background-color: #f6f6f6;
        font-family: sans-serif;
        -webkit-font-smoothing: antialiased;
        font-size: 14px;
        line-height: 1.4;
        margin: 0;
        padding: 0;
        -ms-text-size-adjust: 100%;
        -webkit-text-size-adjust: 100%; 
      }

      table {
        border-collapse: separate;
        mso-table-lspace: 0pt;
        mso-table-rspace: 0pt;
        width: 100%; }
        table td {
          font-family: sans-serif;
          font-size: 14px;
          vertical-align: top; 
      }

      /* -------------------------------------
          BODY & CONTAINER
      ------------------------------------- */

      .body {
        background-color: #f6f6f6;
        width: 100%; 
      }

      /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
      .container {
        display: block;
        margin: 0 auto !important;
        /* makes it centered */
        /*max-width: 580px;*/
        padding: 3px;
		overflow-x: auto;
        width: 1000px; 
      }

      /* This should also be a block element, so that it will fill 100% of the .container */
      .content {
        box-sizing: border-box;
        display: block;
        margin: 0 auto;
        /*max-width: 580px;*/
        padding: 5px; 
      }

      /* -------------------------------------
          HEADER, FOOTER, MAIN
      ------------------------------------- */
      .main {
        background: #ffffff;
        border-radius: 3px;
        width: 100%; 
      }

      .wrapper {
        box-sizing: border-box;
        padding: 5px; 
      }

      .content-block {
        padding-bottom: 10px;
        padding-top: 10px;
      }

      .footer {
        clear: both;
        margin-top: 10px;
        text-align: center;
        width: 100%; 
      }
        .footer td,
        .footer p,
        .footer span,
        .footer a {
          color: #999999;
          font-size: 12px;
          text-align: center; 
      }

      /* -------------------------------------
          TYPOGRAPHY
      ------------------------------------- */
      h1,
      h2,
      h3,
      h4 {
        color: #000000;
        font-family: sans-serif;
        font-weight: 400;
        line-height: 1.4;
        margin: 0;
        margin-bottom: 30px; 
      }

      h1 {
        font-size: 35px;
        font-weight: 300;
        text-align: center;
        text-transform: capitalize; 
      }

      p,
      ul,
      ol {
        font-family: sans-serif;
        font-size: 14px;
        font-weight: normal;
        margin: 0;
        margin-bottom: 15px; 
      }
        p li,
        ul li,
        ol li {
          list-style-position: inside;
          margin-left: 5px; 
      }

      a {
        color: #3498db;
        text-decoration: underline; 
      }

      /* -------------------------------------
          BUTTONS
      ------------------------------------- */
      .btn {
        box-sizing: border-box;
        width: 100%; }
        .btn > tbody > tr > td {
          padding-bottom: 15px; }
        .btn table {
          width: auto; 
      }
        .btn table td {
          background-color: #ffffff;
          border-radius: 5px;
          text-align: center; 
      }
        .btn a {
          background-color: #ffffff;
          border: solid 1px #3498db;
          border-radius: 5px;
          box-sizing: border-box;
          color: #3498db;
          cursor: pointer;
          display: inline-block;
          font-size: 14px;
          font-weight: bold;
          margin: 0;
          padding: 12px 25px;
          text-decoration: none;
          text-transform: capitalize; 
      }

      .btn-primary table td {
        background-color: #3498db; 
      }

      .btn-primary a {
        background-color: #3498db;
        border-color: #3498db;
        color: #ffffff; 
      }

      /* -------------------------------------
          OTHER STYLES THAT MIGHT BE USEFUL
      ------------------------------------- */
      .last {
        margin-bottom: 0; 
      }

      .first {
        margin-top: 0; 
      }

      .align-center {
        text-align: center; 
      }

      .align-right {
        text-align: right; 
      }

      .align-left {
        text-align: left; 
      }

      .clear {
        clear: both; 
      }

      .mt0 {
        margin-top: 0; 
      }

      .mb0 {
        margin-bottom: 0; 
      }

      .preheader {
        color: transparent;
        display: none;
        height: 0;
        max-height: 0;
        max-width: 0;
        opacity: 0;
        overflow: hidden;
        mso-hide: all;
        visibility: hidden;
        width: 0; 
      }

      .powered-by a {
        text-decoration: none; 
      }

      hr {
        border: 0;
        border-bottom: 1px solid #f6f6f6;
        margin: 20px 0; 
      }

      /* -------------------------------------
          RESPONSIVE AND MOBILE FRIENDLY STYLES
      ------------------------------------- */
      @media only screen and (max-width: 620px) {
        table.body h1 {
          font-size: 28px !important;
          margin-bottom: 10px !important; 
        }
        table.body p,
        table.body ul,
        table.body ol,
        table.body td,
        table.body span,
        table.body a {
          font-size: 16px !important; 
        }
        table.body .wrapper,
        table.body .article {
          padding: 10px !important; 
        }
        table.body .content {
          padding: 0 !important; 
        }
        table.body .container {
          padding: 0 !important;
          width: 100% !important; 
        }
        table.body .main {
          border-left-width: 0 !important;
          border-radius: 0 !important;
          border-right-width: 0 !important; 
        }
        table.body .btn table {
          width: 100% !important; 
        }
        table.body .btn a {
          width: 100% !important; 
        }
        table.body .img-responsive {
          height: auto !important;
          max-width: 100% !important;
          width: auto !important; 
        }
      }

      /* -------------------------------------
          PRESERVE THESE STYLES IN THE HEAD
      ------------------------------------- */
      @media all {
        .ExternalClass {
          width: 100%; 
        }
        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {
          line-height: 100%; 
        }
        .apple-link a {
          color: inherit !important;
          font-family: inherit !important;
          font-size: inherit !important;
          font-weight: inherit !important;
          line-height: inherit !important;
          text-decoration: none !important; 
        }
        #MessageViewBody a {
          color: inherit;
          text-decoration: none;
          font-size: inherit;
          font-family: inherit;
          font-weight: inherit;
          line-height: inherit;
        }
        .btn-primary table td:hover {
          background-color: #34495e !important; 
        }
        .btn-primary a:hover {
          background-color: #34495e !important;
          border-color: #34495e !important; 
        } 
      }

    </style>
  </head>
  <body>
    <span class="preheader">CSV Checker</span>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
      <tr>
        <td>&nbsp;</td>
        <td class="container">
          <div class="content">
		  
		  <h1>CSV Checker</h1>
		  <h2>Results</h2>

            <!-- START CENTERED WHITE CONTAINER -->
            <table role="presentation" class="main">

              <!-- START MAIN CONTENT AREA -->
              <tr>
                <td class="wrapper">
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                      <td>
                        <p>Here are the results from CSV Checker.</p>
                        
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                          <tbody>
                            <tr>
                              <td align="left">
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                  <tbody>
                                    <tr>
                                      <td> <a href="http://vojtaripa.pythonanywhere.com/" target="_blank">Go To CSV Checker</a> </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </td>
                            </tr>
                          </tbody>
                        </table>
						
						<h3>File:</h3>
                        <p>"""+myfile+"""</p>
						<br>
						
						<h3>File Path:</h3>
                        <p>"""+str(tempfile_path)+"""</p>
						<br>
						
						<h3>OG Data:</h3>
                        <p>"""+str(df)+"""</p>
						<br>
						
						<h3>Table:</h3>
                        <p>"""+str(df2_no_Nan.to_html())+"""</p>
						<br>
						
						<h3>Input:</h3>
                        <p>"""+info1+"""</p>
						<br>
						
						<h3>Output:</h3>
                        <p>"""+info3+"""</p>
						<br>
                        
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

            <!-- END MAIN CONTENT AREA -->
            </table>
            <!-- END CENTERED WHITE CONTAINER -->

            <!-- START FOOTER -->
            <div class="footer">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                <tr>
                  <td class="content-block">
                    <span class="apple-link">CSV Checker Results - 2022</span>
                    <br> Don't like these emails? email vojtaripa@gmail.com.
                  </td>
                </tr>
                <tr>
                  <td class="content-block powered-by">
                    Created by <a href="http://vojtaripa.pythonanywhere.com/">Vojta Ripa & Scott Roan</a>.
                  </td>
                </tr>
              </table>
            </div>
            <!-- END FOOTER -->

          </div>
        </td>
        <td>&nbsp;</td>
      </tr>
    </table>
  </body>
</html>

          """, subtype='html')

        #### >> Code from here will send the message << ####
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: #Added Gmails SMTP Server
                smtp.login(EmailAdd,Pass) #This command Login SMTP Library using your GMAIL
                smtp.send_message(msg) #This Sends the message
            print ('Email sent successfully!')

        except:
            print ('OH NO! Something went wrong...')


        #now sending all data / results to home.html page:
        return render_template('home.html', results=results, fieldnames=fieldnames, len=len, df2=output, user_csv_b4=user_csv_userinput, mysize=size, highlight_array= highlight, mydf=df2_no_Nan.to_html(), path_info=path_info, http_host=http_host)


"""
print(driver_check(remove_blank_driver(create_driver_list(df_data))))
print(username_check(remove_blank_user(create_user_list(df_data))))
print(blank_licensenumber(df_data))
print(blank_licensestate(df_data))
print(ruleset(df_data))
print(invalid_header(df_data))


1. Potential Issues with your Driver Set Up:
driver_check        = str(print(driver_check(remove_blank_driver(create_driver_list(df_data)))))
username_check      = str(print(username_check(remove_blank_user(create_user_list(df_data)))))

2. Potential Issues with your License Plate Numbers or States
blank_licensenumber = str(print(blank_licensenumber(df_data)))
blank_licensestate  = str(print(blank_licensestate(df_data)))

3. Potential Issues with your Driver Rulesets
ruleset             = str(print(ruleset(df_data)))

4. Potential Issues with your CSV Headers
invalid_header      = str(print(invalid_header(df_data)))
"""


if __name__ == '__main__':
    app.run(debug=True)
