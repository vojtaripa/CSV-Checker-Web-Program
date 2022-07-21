
import pandas as pd

#Section 6: For New Users - Creates Drivers/Username/ID lists and checks for required parameters
state_abbrevs = ['nan', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD' ,'TN', 'TX', 'TT', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY','KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'CM','AL', 'AK', 'AZ', 'AR', 'AS', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS']
time_zones = ['nan','Honolulu - HST', 'Anchorage - AKST/AKDT','Los Angeles - PST/PDT','Phoenix - MST','Denver - MST/MDT','Chicago - CST/CDT','New York - EST/EDT','Halifax - AST/ADT','Azores - AZOT/AZOST','Reykjavik - GMT','London - GMT/BST','Paris - CET/CEST','Kaliningrad - EET','Helsinki - EET/EEST','Turkey - TRT']
driver_status = ['nan', 'active', 'deactivated']


def create_driver_list(df_data, output, highlight):
    driver_list = df_data['name'].tolist()
    driver_list2 = []
    for i in driver_list:
        if i not in driver_list2:
            driver_list2.append(i)
        else:
            print('There are two users in your CSV file with the name ' + i)
            output.append('There are two users in your CSV file with the name ' + str(i))
            highlight.append(str(i))
    return driver_list2


def create_user_list(df_data,output,highlight):
  username_list = df_data['username'].tolist()
  username_list2 = []
  for i in username_list:
        if str.lower(i) not in username_list2:
            username_list2.append(str.lower(i))
        else:
            print('There are two users in your CSV file with the username ' + i)
            output.append('There are two users in your CSV file with the username ' + str(i))
            highlight.append(str(i))
  return username_list

def remove_blank_user(u_list,output,highlight):
  n = 0
  for name in u_list: 
    if n < len(u_list):
      if type(name) == float:
        print('The cell for Username on Row ' + str(n + 1) + ' is blank')
        output.append('The cell for Username on Row ' + str(n+1) + ' is blank')
        highlight.append(str(n+1))
        n += 1
      else: 
        n+= 1
  new_user_list = [x for x in u_list if pd.isnull(x) == False]
  return(new_user_list)


def remove_blank_driver(d_list,output,highlight):
  n = 0
  for name in d_list: 
    if n < len(d_list):
      if type(name) == float:
        print('The cell for Driver Name on Row ' + str(n + 1) + ' is blank')
        output.append('The cell for Driver Name on Row ' + str(n+1) + ' is blank')
        highlight.append(str(n+1))
        n += 1
      else: 
        n+= 1
  newlist = [x for x in d_list if pd.isnull(x) == False]
  return(newlist)

def username_check(u_check,output,highlight):
    incompatible_characters = '`!@#$%^&*()_+=\|]}[{:;/?><'
    n = 0
    for u in u_check:
        n += 1
        if type(u) != int: 
          res = ' ' in u
          if res == True:
            print('There is a space in the username ' + u + ' located in row ' + str(n + 1))
            output.append('There is a space in the username ' + str(u) + ' located in row ' + str(n+1))
            highlight.append(str(u))
          if any(s in incompatible_characters for s in u):
            print('There is an incompatible character in the username ' + u + ' located in row ' +  str(n + 1))
            output.append('There is an incompatible character in the username ' + str(u) + ' located in row' + str(n+1))
            highlight.append(str(u))
          if len(u) < 4:
            print('Username ' + u + ' is less than 4 characters and is located in row ' + str(n + 1))
            output.append('Username ' + str(u) + ' is less than 4 characters and is located in row ' + str(n+1))
            highlight.append(str(u))
    return ' '


def driver_check(d_check, output, highlight):
    incompatible_characters = '`~!@#$%^*()_+=\|]}[{:;/?><'
    n = 0
    for c in d_check:
        res = '  ' in c
        n += 1
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


def blank_licensenumber(name_check,df_data, output, highlight):
    licensenumber_list = df_data['license number'].tolist()
    licensestate_list = df_data['license state'].tolist()
    n = 0
    upper_state = []
    state_abbrev_rows = []
    number_rows = []
    state_rows = []
    for x in licensestate_list:
      if str(x) != 'nan':
        upper_state.append(x.upper())
    num_len= len(licensenumber_list)
    for name in licensenumber_list:
        if n < num_len:
            if str(name) == 'nan' and str(licensestate_list[n]) != 'nan':
                if str(licensestate_list[n]) not in state_abbrevs:
                    n += 1
                    state_abbrev_rows.append(n+1)
                else:                
                    n += 1
                    state_rows.append(n+1)
            elif str(name) != 'nan' and str(licensestate_list[n]) == 'nan':
                if str(licensestate_list[n]) not in state_abbrevs:
                    n += 1
                    state_abbrev_rows.append(n +1)
                else: 
                    n += 1
                    number_rows.append(n +1)
            elif str(name) != 'nan' and str(licensestate_list[n]) != 'nan':
                if str(licensestate_list[n]) not in state_abbrevs:
                    n += 1
                    state_abbrev_rows.append(n+1)
                else: 
                    n += 1              
            else: 
                n += 1
        if n >= num_len:
          if len(state_abbrev_rows) > 10:
            print('There are unacceptable state abbreviations in rows ' + str(state_abbrev_rows))
            output.append('There are unacceptable state abbreviations in rows ' + str(state_abbrev_rows))
            highlight.append(str(state_abbrev_rows))
          if len(state_rows) > 10:
            print('There are License States set but no License Numbers in rows ' + str(state_rows))
            output.append('There are License States set but no License Numbers in rows ' + str(state_rows))
            highlight.append(str(state_rows))
          if len(number_rows) > 10: 
            print('There are License Numbers set but no License States in rows ' + str(number_rows))
            output.append('There are License Numbers set but no License States in rows ' + str(number_rows))
            highlight.append(str(number_rows))
          if(len(state_abbrev_rows) <= 10):
            for y in range(len(state_abbrev_rows)):
                  print('There is an unacceptable state abbreviation in row ' + str(state_abbrev_rows[y]))
                  output.append('There is an unacceptable state abbreviation in row ' + str(state_abbrev_rows[y]))
                  highlight.append(str(state_abbrev_rows))
          if len(state_rows) < 10:
            for z in range(len(state_rows)):
               print('There are License States set but no License Numbers in rows ' + str(state_rows[z]))
               output.append('There are License States set but no License Numbers in rows ' + str(state_rows[z]))
               highlight.append(str(state_rows[z]))
          if len(number_rows) < 10: 
            for a in range(len(number_rows)):
              print('There are License Numbers set but no License States in rows ' + str(state_rows[a])) 
              output.append('There are License Numbers set but no License States in rows ' + str(state_rows[a]))
              highlight.append(str(state_rows[a]))
    return ' '

#Section 7: This section checks that the set driver ruleset matches rulesets in the system
          #Add check that makes sure that there is a State set in the next column
Samsara_Driver_Rulesets = ['USA Property (7/60)', 'USA Passenger (8/70)','USA Passenger (7/60)','Alaska Property (8/80)','Alaska Property (7/70)','Alaska Passenger (8/80)','Alaska Passenger (7/70)','Nebraska (8/80)','North Carolina (8/80)','North Carolina (7/70)','Oklahoma (8/70)','Oklahoma (7/60)','Oregon (8/80)','Oregon (7/70)','South Carolina (8/80)','South Carolina (7/70)','Texas (7/70)','Wisconsin (8/80)','Wisconsin (7/70)','California School/FLV (8/80)','California Farm (8/112)','California Property (8/80)','California Flammable Liquid (8/80)','California Passenger (8/80)','California Motion Picture (8/80)','Florida (8/80)', 'Florida (7/70)']
Allowable_Restarts = ['34-hour Restart', '24-hour Restart','None', 'nan','',' ']
Allowable_Restbreaks = ['Property (on-duty/off-duty/sleeper)','None','California Mealbreak (off-duty/sleeper)','nan','',' ']

def ruleset(df_data, output, highlight):
    if 'driver ruleset cycle' in df_data:
        uploaded_ruleset = df_data['driver ruleset cycle'].tolist()
        uploaded_ruleset_state = df_data['driver ruleset us state to override'].tolist()
        ruleset_rows = []
        uploaded_driver_ruleset_restart = df_data['driver ruleset restart'].tolist()
        uploaded_driver_rulset_restbreak = df_data['driver ruleset restbreak'].tolist()
        n = 0
        q = 0
        v = 0
        length = len(uploaded_ruleset) - 1
        for c in uploaded_ruleset:
            if str(c) != 'nan':
                if c not in Samsara_Driver_Rulesets:
                    n +=1
                    ruleset_rows.append(n+1)
                if c in Samsara_Driver_Rulesets:
                    if str(uploaded_ruleset_state[n]) == 'nan':
                        print("You have a driver ruleset without a state set in row " + str(n+1) + '. If this is not a federal override, please set a state.')
                        output.append('You have a driver ruleset without a state set in row ' + str(n+1) + 'If this is not a federal override, please set a state.')
                        highlight.append(str(n+1))
                        n +=1
                    else: 
                        n +=1
            elif str(c) == 'nan':
                if str(uploaded_ruleset_state[n]) != 'nan':
                    if str(uploaded_ruleset_state[n]) in state_abbrevs:
                      print('There is a Ruleset State but no Ruleset set in row ' + str(n+1)  )
                      output.append('There is a Ruleset State but no Ruleset set in row ' + str(n+1))
                      highlight.append(str(n+1))
                      n +=1
                    else: 
                      print('The State Abbreviation of ' + str(uploaded_ruleset_state[n]) + ' in row ' + str(n+1) + ' is not a valid State Abbreviation. Please update it.')
                      output.append('The State Abbreviation of ' + str(uploaded_ruleset_state[n]) + ' in row ' + str(n+1) + ' is not a valid State Abbreviation. Please update it.')
                      n += 1
                else:
                    n += 1
            if str(n) == str(length):
              if len(ruleset_rows) > 10:
                print('There are unacceptable rulesets on the following rows:', ruleset_rows)
                output.append('There are unacceptable rulesets on the following rows:', ruleset_rows)
                highlight.append(ruleset_rows)
              else: 
                for y in range(len(ruleset_rows)):
                  print('The ruleset that is set in row ' + str(ruleset_rows[y]) + ' is not a valid ruleset. Please check that there is a custom ruleset set or set the ruleset to one of the rulesets in the article:https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts')
                  output.append('The ruleset that is set in row ' + str(ruleset_rows[y]) + ' is not a valid ruleset. Please check that there is a custom ruleset set or set the ruleset to one of the rulesets in the article:https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts')
                  highlight.append(str(ruleset_rows[y]))
        for x in uploaded_driver_rulset_restbreak:
            if str(x) not in Allowable_Restbreaks:
                print('The Ruleset Restbreak that you have set in row ' + str(q+1) + ' is not an allowable restbreak. Please set it to be one of these options: ' + str(Allowable_Restbreaks))
                output.append('The Ruleset Restbreak that you have set in row ' + str(q+1) + ' is not an allowable restbreak. Please set it to be one of these options: ' + str(Allowable_Restbreaks))
                highlight.append(str(q+1))
                q += 1
        for y in uploaded_driver_ruleset_restart:
            if str(y) not in Allowable_Restarts: 
                print('The Ruleset Restart that you have set in row ' + str(v+1) + ' is not a valid Restart. Please set it to be one of these options: ' + str(Allowable_Restarts))   
                output.append('The Ruleset Restart that you have set in row ' + str(v+1) + ' is not a valid Restart. Please set it to be one of these options: ' +  str(Allowable_Restarts)) 
                highlight.append(str(v+1))
                v += 1
    else:
        print('No Rulesets')
    return ' '
            

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

def invalid_header(hlist, output, highlight):
  current_hlist = list(hlist)
  n = 0
  invalid_header_rows = []
  if n < len(current_hlist):
    for x in current_hlist:
      if x[0:7] != 'unnamed': 
        if x not in header_list:
          n += 1
          invalid_header_rows.append(str.title(x))
        else: 
          n += 1 
      if x[0:7] == 'unnamed' :
        print('There is a blank header in between the headers ' + str.title(current_hlist[n-1]) + ' and ' + str.title(current_hlist[n+1]) +'. Please delete the column or fill in the header.')
        output.append('There is a blank header in between the headers ' + str.title(current_hlist[n-1]) + ' and ' + str.title(current_hlist[n+1]) +'. Please delete the column or fill in the header.')
        n += 1
  if n >= len(current_hlist):
    if len(invalid_header_rows) >= 10:
        print('The following headers are invalid: ' + str(invalid_header_rows))
        output.append('The following headers are invalid: ' + str(invalid_header_rows))
        highlight.append(str(invalid_header_rows))
    if len(invalid_header_rows) < 10:
      for z in range(len(invalid_header_rows)):
        print('The header ' + str(invalid_header_rows[z]) + 'is not a recognized header. Please update this to match the guide found here: https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts')
        output.append('The header ' + str(invalid_header_rows[z]) + 'is not a recognized header. Please update this to match the guide found here: https://kb.samsara.com/hc/en-us/articles/4402804484621-Manage-Driver-Accounts')
        highlight.append(str(invalid_header_rows[z]))
  return ' '


def timezone_check(df_data,output,highlight):
  tz_list = df_data['home terminal timezone'].tolist()
  n = 0
  tz_rows = []
  for x in tz_list:
    if n < len(tz_list):
      if str(x) not in time_zones:
        n += 1
        tz_rows.append(n + 1)     
      else: 
        n += 1
    if n >= len(tz_list):
          if len(tz_rows) >= 10:
            print('The Time Zones in rows ' + str(tz_rows) + ' are invalid.')
            output.append('The Time Zones in rows ' + str(tz_rows) + ' are invalid.')
            highlight.append(str(tz_rows))
          if len(tz_rows) < 10:
            for a in range(len(tz_rows)):
              print('The Time Zone  on row ' + str(tz_rows[a]) +  ' is not an allowable timezone.')    
              output.append('The Time Zone  on row ' + str(tz_rows[a]) +  ' is not an allowable timezone.')
              highlight.append(str(tz_rows[a]))
  return ' '

def start_time(df_data,highlight, output):
  st_list = df_data['eld day start hour'].tolist()
  n = 0
  st_rows = []
  for x in st_list: 
    if n < len(st_list):
      if x == 0: 
        n += 1
      elif x == 12:
        n += 1
      elif str(x) == 'nan':
        n += 1
      else:
        n += 1
        st_rows.append(n+1)
    if n >= len(st_list):
      if len(st_rows) >= 10:
        print('The ELD Day Start Hours in rows ' + str(st_rows) + ' are invalid. Please update these times to either be 0, 12 or leave blank.')
        output.append('The ELD Day Start Hours in rows ' + str(st_rows) + ' are invalid. Please update these times to either be 0, 12 or leave blank.')
        highlight.append(str(st_rows))
      if len(st_rows) < 10:
        for a in range(len(st_rows)):
          print('The ELD Day Start Hour in row ' + str(st_rows[a]) + ' is invalid. Please update the time to be 0, 12 or leave blank')      
          output.append('The ELD Day Start Hour in row ' + str(st_rows[a]) + ' is invalid. Please update the time to be 0, 12 or leave blank')
          highlight.append(str(st_rows[a]))  
  return ' '

def driverstatus(df_data, output, highlight):
  n = 0
  ds_list = df_data['driver status'].tolist()
  ds_rows = []
  for x in ds_list: 
    if n < len(ds_list):
      if str(x) not in driver_status:
        n += 1
        ds_rows.append(n+1)
      else: 
        n += 1
    if n >= len(ds_list):
        if len(ds_rows) >= 10:
          print('The driver statuses in rows ' + str(ds_rows) + ' are invalid. Please correct them to Acitve, Deactivated or leave blank')
          output.append('The driver statuses in rows ' + str(ds_rows) + ' are invalid. Please correct them to Acitve, Deactivated or leave blank')
          highlight.append(str(ds_rows))
        if len(ds_rows) < 10:
          for a in range(len(ds_rows)):
            print('The ELD Day Start Hour in row ' + str(ds_rows[a]) + ' is invalid. Please correct it to Acitve, Deactivated or leave blank')
            output.append('The ELD Day Start Hour in row ' + str(ds_rows[a]) + ' is invalid. Please correct it to Acitve, Deactivated or leave blank')
            highlight.append(str(ds_rows[a]))
  return ' '    