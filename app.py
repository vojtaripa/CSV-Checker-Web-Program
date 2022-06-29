from flask import Flask, render_template, request
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


#from io import StringIO

app = Flask(__name__)

scroll=False

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        results = []
        results2 = []
        output = []
        highlight = []

        tempfile_path = "none"
        file = "none"



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

        print(feedback_name)
        

        #Gets the TEXTBOX variable from textarea then based on if there is text or not it will proceed slitly differently
        user_csv_userinput = request.form.get('user_csv')
        
        '''
        if feedback_name != "":
          df_data_vojta = ""
          feedback_name = feedback_name #do nothing right now.
          return render_template('home.html', df2=feedback_name)
        '''
        #//////////////////////////////////////////////////////////
        #executing FILE UPLOAD (Doesnt Quite work with some files)
        #//////////////////////////////////////////////////////////
        if user_csv_userinput == "":
        

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
          df = pd.read_csv(tempfile_path) #, encoding='cp1252'

          df2 = df.rename(str.lower, axis='columns')

          df_data_vojta = pd.DataFrame(df2)

          
          #NOW TO MAKE TABLE ON NEXT PAGE:
          table_data = df2 #sheet
          reader = csv.DictReader(table_data)

          for row in reader:
              results.append(dict(row))

          fieldnames = [key for key in results[0].keys()]

        


        #//////////////////////////////////////////////////////////
        #IF uploading from textbox directly (WORKS)
        #//////////////////////////////////////////////////////////
        else:
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



        #Section 6: For New Users - Creates Drivers/Username/ID lists and checks for required parameters
        
        def create_driver_list(CSV_file):
            driver_list = df_data['name'].tolist()
            driver_list2 = []
            for i in driver_list:
                if i not in driver_list2:
                    driver_list2.append(i)
                else:
                    print('There are two users in your CSV file with the name'+ i)
                    output.append('There are two users in your CSV file with the name ' + i)
                    highlight.append(i)
            return driver_list2
        
        
        def create_user_list(CSV_User_File):
          username_list = df_data['username'].tolist()
          username_list2 = []
          for i in username_list:
                if i not in username_list2:
                    username_list2.append(i)
                else:
                    print('There are two users in your CSV file with the username'+ i)
                    output.append('There are two users in your CSV file with the username ' + i)
                    highlight.append(i)
          return username_list
        
        def remove_blank_user(u_list):
          n = 0
          for name in u_list:
            if n < len(u_list):
              if type(name) == float:
                print('The cell for Username on Row', str(n + 1), 'is blank')
                output.append('The cell for Username on Row ' + str(n + 1) + ' is blank')
                highlight.append(str(n + 1))
                n += 1
              else:
                n+= 1
          new_user_list = [x for x in u_list if pd.isnull(x) == False]
          return(new_user_list)
        
        
        def remove_blank_driver(d_list):
          n = 0
          for name in d_list:
            if n < len(d_list):
              if type(name) == float:
                print('The cell for Driver Name on Row'+str(n + 1)+ 'is blank')
                output.append('The cell for Driver Name on Row ' + str(n + 1) + ' is blank')
                highlight.append(str(n + 1))
                n += 1
              else:
                n+= 1
          newlist = [x for x in d_list if pd.isnull(x) == False]
          return(newlist)
        
        
        def username_check(u_check):
            incompatible_characters = '`!@#$%^&*()_+=\|]}[{:;/?><'
            n = 0
            for u in u_check:
                n += 1
        
            if type(u) != int: 	
                  res = ' ' in u	
                  if res == True:	
                    print('There is a space in the username ' + u + ' located in row ' + str(n + 1))	
                    output.append('There is a space in the username ' + u + ' located in row ' + str(n+1))
                    highlight.append(u)			
                  if any(s in incompatible_characters for s in u):	
                    print('There is an incompatible character in the username ' + u + ' located in row ' +  str(n + 1))	
                    output.append('There is an incompatible character in the username ' + u + ' located in row' + str(n+1))
                    highlight.append(u)
                  if len(u) < 4:	
                    print('Username ' + u + ' is less than 4 characters and is located in row ' + str(n + 1))	
                    output.append('Username ' + u + ' is less than 4 characters and is located in row ' + str(n+1))
                    highlight.append(u)
            return ' '
            
        
        
        def driver_check(d_check):
            incompatible_characters = '`~!@#$%^*()_+=\|]}[{:;/?><' # got rid of &
            n = 0
            for c in d_check:
                res = '  ' in c
                n += 1
                d = n + 1
                if res == True:
                  print('There are two spaces in the name ' + c + ' located in row ' + str(n+1))	
                  output.append('There is a space in the name ' + c + ' located in row ' + str(n+1))
                  highlight.append(c)
                if any(s in incompatible_characters for s in c):
                  print('There is an incompatible character in the name ' + c + ' located in row' + str(n+1))	
                  output.append('There is an incompatible character in the name ' + c + ' located in row' + str(n+1))
                  highlight.append(c)
                if c[-1] == ' ':
                  print('There is a space at the end of the name '+ c + ' located in row ' + str(n+1))	
                  output.append('There is a space at the end of the name ' + c + ' located in row ' + str(n+1))
                  highlight.append(c)
            return ' '
        
        #function that used api was here
        
        def double_name(name_check):
          new_driver_list = df_data['name'].tolist()
          new_id_list = df_data['id'].tolist()
          n = 0
          for i in new_driver_list:
            if i in driver_list:
              if new_id_list[n] not in id_list:
                print('There is an existing user with the name', i, 'whose id does not match what is on the dashboard. Please double check that')
                output.append('There is an existing user with the name ' + i + ' whose id does not match what is on the dashboard. Please double check that ')
                highlight.append(i)
                n +=1
              else:
                n += 1
            else:
              n += 1
        
        
        def blank_licensenumber(ln_check):
          licensenumber_list = df_data['license number'].tolist()	
          licensestate_list = df_data['license state'].tolist()	
          n = 0	
          for name in licensenumber_list: 	
            if n < len(licensenumber_list):	
              if str(name) == 'nan' and type(licensestate_list[n]) != float:	
                print('There is no License Number set on row' + str(n+1) + ' but there is a License State set. Please set a license number for this User')	
                output.append('There is not License Number set on row ' + str(n+1) + ' but there is a License State set. Please set a license number for this User')
                highlight.append(str(n + 1))		
                n += 1	
              else: 	
                n+= 1	
          return ' '
        
        
        def blank_licensestate(ls_check):
          licensestate_list = df_data['license state'].tolist()	
          licensenumber_list = df_data['license number'].tolist()	
          n = 0	
          for name in licensestate_list: 	
            if n < len(licensestate_list):	
              if type(name) == float and str(licensenumber_list[n]) != 'nan':	
                print('There is no License State set on row', n + 1,'but there is a License Number set. Please set a license state for this User')	
                output.append('There is no License State set on row ' + str(n+1) + ' but there is a License Number set. Please set a license state for this User')
                highlight.append(str(n + 1))
                n += 1	
              else: 	
                n+= 1	
          return ' ' 
        
        
        #Section 7: This section checks that the set driver ruleset matches rulesets in the system	
                  #Add check that makes sure that there is a State set in the next column	
        Samsara_Driver_Rulesets = ['USA Property (7/60)', 'USA Passenger (8/70)','USA Passenger (7/60)','Alaska Property (8/80)','Alaska Property (7/70)','Alaska Passenger (8/80)','Alaska Passenger (7/70)','Nebraska (8/80)','North Carolina (8/80)','North Carolina (7/70)','Oklahoma (8/70)','Oklahoma (7/60)','Oregon (8/80)','Oregon (7/70)','South Carolina (8/80)','South Carolina (7/70)','Texas (7/70)','Wisconsin (8/80)','Wisconsin (7/70)','California School/FLV (8/80)','California Farm (8/112)','California Property (8/80)','California Flammable Liquid (8/80)','California Passenger (8/80)','California Motion Picture (8/80)','Florida (8/80)', 'Florida (7/70)']	
        Allowable_Restarts = ['34-hour Restart', '24-hour Restart','None']	
        Allowable_Restbreaks = ['Property (on-duty/off-duty/sleeper)','None','California Mealbreak (off-duty/sleeper)']	
        Allowable_Restarts_str = '34-hour Restart, 24-hour Restart, None'
        Allowable_Restbreaks_str = 'Property (on-duty/off-duty/sleeper), None, California Mealbreak (off-duty/sleeper)'	
        
        def ruleset(dvrs):	
          if 'driver ruleset cycle' in df_data:	
            uploaded_ruleset = df_data['driver ruleset cycle'].tolist()	
            uploaded_ruleset_state = df_data['driver ruleset us state to override'].tolist()	
            ruleset_rows = []	
            uploaded_driver_ruleset_restart = df_data['driver ruleset restart'].tolist()	
            uploaded_driver_rulset_restbreak = df_data['driver ruleset restbreak'].tolist()	
            n = 0	
            q = 0	
            v = 0	
            for c in uploaded_ruleset:	
                	
                if str(c) != 'nan':	
                  if c not in Samsara_Driver_Rulesets:	
                    ruleset_rows.append(n+1)	
                    n += 1	
                  if c in Samsara_Driver_Rulesets:	
                    if str(uploaded_ruleset_state[n]) == 'nan':	
                      print("You have a driver ruleset without a state set in row " + str(n+1) + '. If this is not a federal override, please set a state.')	
                      output.append('You have a driver ruleset without a state set in row ' + str(n+1) + 'If this is not a federal override, please set a state.')	
                      n +=1	
                if str(c) == 'nan':	
                  if str(uploaded_ruleset_state[n]) != 'nan':	
                    print('There is a Ruleset State but no Ruleset set in row ' + str(n+1)  )	
                    output.append('There is a Ruleset State but no Ruleset set in row ' + str(n+1))	
                    n +=1	
                if n >= len(uploaded_ruleset):	
                  print('There are invalid rulesets on the following rows: ' + str(ruleset_rows))	
                  output.append('There are invalid rulesets on the following rows: ' + str(ruleset_rows))	
                  n +=1	
                  return ' '	
            for x in uploaded_driver_rulset_restbreak:	
              if x not in Allowable_Restbreaks:	
                print('The Ruleset Restbreak that you have set in row ' + str(q+1) + ' is not an allowable restbreak. Please set it to be one of these options: ' + str(Allowable_Restbreaks))	
                output.append('The Ruleset Restbreak that you have set in row ' + str(q+1) + ' is not an allowable restbreak. Please set it to be one of these options: ' + str(Allowable_Restbreaks_str))	
                q += 1	
            for y in uploaded_driver_ruleset_restart:	
              if y not in Allowable_Restarts: 	
                print('The Ruleset Restart that you have set in row ' + str(v+1) + ' is not a valid Restart. Please set it to be one of these options: ' + str(Allowable_Restarts))   	
                output.append('The Ruleset Restart that you have set in row ' + str(v+1) + ' is not a valid Restart. Please set it to be one of these options: ' +  str(Allowable_Restarts_str)) 	
                v += 1	
          else:	
            print('No Rulesets')	
          return ' '
        
        '''
        def ruleset(dvrs):
          uploaded_ruleset = df_data['driver ruleset cycle'].tolist()
          uploaded_ruleset_state = df_data['driver ruleset us state to override'].tolist()
          n = 0
          for c in uploaded_ruleset:
            n += 1
            if type(c) != float:
              if c not in Samsara_Driver_Rulesets:
                print(c,'is not a valid ruleset. Please update the Driver Ruleset in row', n+1, 'to a valid ruleset or create a custom driver ruleset. A list of valid rulesets can be found at https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts')
                output.append(str(c)+' is not a valid ruleset. Please update the Driver Ruleset in row '+ str(n+1) + ' to a valid ruleset or create a custom driver ruleset. A list of valid rulesets can be found at https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts') #REPLACE
                highlight.append(c)
            if type(c) == float:
              if type(uploaded_ruleset_state[n-1]) != float:
                print('There is a Ruleset State but no Ruleset set in row', n + 1 )
                output.append('There is a Ruleset State but no Ruleset set in row ' + str(n + 1))
        '''
        
        
        #Section 8: This Section checks that the headers used in the CSV File are allowed
        header_list = \
        	['id', 'username', 'password', 'name', 'phone', 'notes', 'license number', 	
         'license state', 'eld exempt', 'eld exempt reason', 	
         '16-hour short-haul exemption', 'adverse driving exemption', 	
         'defer off-duty exemption', 'adverse driving (canada) exemption', 	
         'eld personal conveyance (pc)', 'eld yard moves (ym)', 'eld utility exemption', 	
         'waiting time (wt)', 'eld day start hour', 'home terminal timezone', 	
         'carrier name override','main office address override',	
         'carrier us dot number override','home terminal name','home terminal address',	
         'peer group tag','vehicle selection tag','trailer selection tag','id card code'	
         ,'tachograph card','driver status','tags','attributes',	
         'us short haul exemption','driver id','driver ruleset cycle',	
         'driver ruleset us state to override','driver ruleset restart','driver ruleset restbreak','driver id token', 'peer group', 'start of day workflow', 'end of day workflow']
        def invalid_header(hlist):
          current_hlist = list(hlist)
          n = 0
          for x in current_hlist:
            if x[0:7] != 'unnamed': 	
              if x not in header_list:	
                print('The header ' + str.title(x) + ' is not a recognized header. Please update this to match the guide found here: https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts')	
                output.append('The header ' + str.title(x) + ' is not a recognized header. Please update this to match the guide found here: https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts')
                highlight.append(str(str.title(x)))
                n += 1
              else:
                n += 1
            if x[0:7] == 'unnamed' :
              print("unnamed")
              print('There is a blank header in between the headers', str.title(current_hlist[n-1]), 'and', str.title(current_hlist[n+1]),'Please delete the column or fill in the header.')
              #output.append('There is a blank header in between the headers ' + str((str.current_hlist[n-1])) + ' and ' + str.title(current_hlist[n+1]) + ' Please delete the column or fill in the header.')
              output.append('There is a blank header in between the headers ' + str.title(current_hlist[n-1]) + ' and ' + str.title(current_hlist[n+1]) +'. Please delete the column or fill in the header.')
              n += 1
          return ' '

        #******************************************************************************************************************************************************

        """
        # THESE 2 use API:
        def id_present(id_check):
          new_id_list = df_data['id'].tolist()
          password_list = df_data['password'].tolist()
          new_user_list = df_data['username'].tolist()
          new_driver_list = df_data['name'].tolist()
          n = 0
          for i in new_id_list:
            if str(i) != 'nan':
                if i not in id_list:
                    print('You have assigned user', new_driver_list[n], 'an ID that is not in your dashboard. Please edit the id in row', n+1)
                    n += 1
            elif str(i) == 'nan':
                if new_user_list[n] not in user_list:
                    if type(password_list[n]) == float:
                        print('There is no password present for new driver', new_driver_list[n], 'in row', n+1)
                        n += 1
                    else:
                        n+= 1
                elif new_user_list[n] in user_list:
                    print('There is an existing user name, ', new_user_list[n],'on row', n, 'that is already on the dash. Update username or make the ids match')
                    n +=1
                elif type(new_user_list[n]) == float:
                    print('There is no user set in row',n)
                else:
                    n += 1
        # END CHECK
        """




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
        output.append('1. Potential Issues with your Driver Set Up:')
        driver_check        = driver_check(remove_blank_driver(create_driver_list(df_data_vojta)))
        username_check      = username_check(remove_blank_user(create_user_list(df_data_vojta)))


        #2. Potential Issues with your License Plate Numbers or States
        output.append('2. Potential Issues with your License Plate Numbers or States:')
        blank_licensenumber = blank_licensenumber(df_data_vojta)
        blank_licensestate  = blank_licensestate(df_data_vojta)


        #3. Potential Issues with your Driver Rulesets
        output.append('3. Potential Issues with your Driver Rulesets:')
        ruleset             = ruleset(df_data_vojta)


        #4. Potential Issues with your CSV Headers
        output.append('4. Potential Issues with your CSV Headers:')
        invalid_header      = invalid_header(df_data_vojta)

        print("Object type: \n")
        print(df_data_vojta)
        print("\n \n")


        #print("value of output: " + output)
        pretty_output = pprint.pprint(output)

        #size is how many errors I have, Ignooring the 4 titles / functions I'm running
        size = (len(output)-4)

        #EMAIL STUFF
        #////////////////////////////////////////////////////////////////////////////////////
        info1 = df_data.to_string()
        info2 = "\n".join(output)
        body1 = 'File: '+str(file.name)+'Filepath\n' + str(tempfile_path) + '\n\nOG Data:\n\n'+str(df)+'\n\nInput:\n\n' + info1 + '\n\nOutput:\n\n'+ info2
        #body = ('Input:\n\n', df_data,'- Output:\n\n', output)
        
        EmailAdd = "vojtaripa@gmail.com" #senders Gmail id over here
        Pass = "rnlnndgxawzdrejh" #senders Gmail's Password over here 

        msg = EmailMessage()
        msg['Subject'] = ('CSV Checker Results - '+str(file)) # Subject of Email
        msg['From'] = EmailAdd
        msg['To'] = ['vojtaripa@gmail.com', 'vojta.ripa@samsara.com'] # Reciver of the Mail
        msg.set_content(body1) # Email body or Content

        #### >> Code from here will send the message << ####
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: #Added Gmails SMTP Server
                smtp.login(EmailAdd,Pass) #This command Login SMTP Library using your GMAIL
                smtp.send_message(msg) #This Sends the message
            print ('Email sent successfully!')

        except:
            print ('OH NO! Something went wrong...')


        #now sending all data / results to home.html page:
        return render_template('home.html', results=results, fieldnames=fieldnames, len=len, df2=output, user_csv_b4=user_csv_userinput, mysize=size, highlight_array= highlight)


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
