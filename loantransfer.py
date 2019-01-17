#!/usr/bin/python
#
# loantransfer.py
# 2019 by Nazzareno Bedini - University of Pisa
# For Alma Ex Libris ILS
# inspired by this Alma Tech blog post: https://developers.exlibrisgroup.com/blog/Alma-Bulk-Loan-Transfer-Using-Analytics-and-Offline-Circ
# usage: python loantransfer.py user_id_from user_id_to
# create one or more file .dat to bulk loans transfer from a user to another user: the .dat file/s has to be uploaded in Alma offline circulation tool.
#
import sys
import requests
import time
from xml.etree import ElementTree 
from datetime import datetime, timedelta

# ini section: give your api key and api server as indicated in https://developers.exlibrisgroup.com/alma/apis
api_user_key = "[institution api key]";
api_baseurl = "https://api-eu.hosted.exlibrisgroup.com";
# if you want you can personalize here the basename of .dat file and the help usage text
basename_datfile = "LoanTransfer_"
usage_text = "Usage:\npython loantransfer.py user_id_from user_id_to\npython loantransfer.py -h for help"
# end ini section

# return a xml object from web api
def get_xmlobj(api_url):
    try:
        response = requests.get(api_url)
    except requests.exceptions.RequestException as e:  
        sys.exit("Error on api get info, please check you connection and retry:\n" + str(e))
    response_obj = ElementTree.fromstring(response.content)
    return response_obj

# return a row for offline circulation file formatted as indicated in https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/030Fulfillment/070Advanced_Tools/060Offline_Circulation
# note: adjuste loan time/date according to UTC timezone and adding 1 minute for restitution and 2 minutes for reloan.
def offline_format_row(date_loan, barcode, user_id=False):    
    utc_offset = -time.timezone/3600
    date_r = datetime.strptime(date_loan[0:16], "%Y-%m-%dT%H:%M") + timedelta(hours=utc_offset) + timedelta(minutes=1)
    if (not user_id):
        # this is the restitution of the item row
        return date_r.strftime("%Y%m%d%H%M") + 'R' + barcode
    date_l = datetime.strptime(date_loan[0:16], "%Y-%m-%dT%H:%M") + timedelta (hours=utc_offset) + timedelta(minutes=2)
    n_spaces = 80 - len(barcode)
    # giving the user_id to transfer the loan you obtain the loan row
    return date_l.strftime("%Y%m%d%H%M") + "L" + barcode + " "*n_spaces + user_id

print ("\n*** Transfer loans from an user to another one in conjuction with Alma Offline Circulation ***\n")

#print help user invoke by:
#loantransfer.py -h, loantransfer.py help, loantransfer.py -help, loantransfer.py --help
help_strings = {'help', '-h', '--help', "-help"}
if sys.argv[1] in help_strings:
    sys.exit(usage_text)

if len(sys.argv) < 3:
    sys.exit("Error, need at least two arguments.\n" + usage_text)
if len(sys.argv) > 3:
    print("Warn: extra argument ignored.\n" + usage_text)

# check if both users exists in Alma
url_userfrom = api_baseurl + '/almaws/v1/users/' + sys.argv[1]
url_userto = api_baseurl + '/almaws/v1/users/' + sys.argv[2]
queryParams = "?user_id_type=all_unique&view=brief&expand=none&apikey=" + api_user_key

user_alma_from = get_xmlobj(url_userfrom + queryParams)
user_alma_to = get_xmlobj(url_userto + queryParams)
try:
    user_from_name = user_alma_from.find("last_name").text + " " + user_alma_from.find("first_name").text
    user_to_name = user_alma_to.find("last_name").text + " " + user_alma_to.find("first_name").text
except:
    sys.exit("Error, no user/s found in Alma.")

print ("Transferring loans from user " + user_from_name + " (" + user_alma_from.find("primary_id").text + ") to user " + user_to_name + " (" +  user_alma_to.find("primary_id").text + ")")

url_userloan = url_userfrom + "/loans"
queryParams = "?user_id_type=all_unique&limit=100&apikey=" + api_user_key;
loans_obj = get_xmlobj(url_userloan + queryParams)
r_offline_circ = {}
l_offline_circ = {}
loan_count = 0
for item_loan in loans_obj.iter("item_loan") :
    circ_desk = item_loan.find("circ_desk").text
    # sometime circ_desk could be not defined
    if (not circ_desk):
        circ_desk = "NO_CIRC_DESK"
    key_lib_circ = item_loan.find("library").text + "_" + circ_desk
    r_offline_circ.setdefault(key_lib_circ, []).append(offline_format_row(item_loan.find("loan_date").text, item_loan.find("item_barcode").text) + "\n")
    l_offline_circ.setdefault(key_lib_circ, []).append(offline_format_row(item_loan.find("loan_date").text, item_loan.find("item_barcode").text, user_alma_to.find("primary_id").text) + "\n")
    loan_count += 1

# if user_from has no active loans, exit
if loan_count == 0 :
    sys.exit("No user loans found in Alma")
print ("Found " + str(loan_count) + " loans to transfer")

# create a .dat file for every library/circ desk (you have to upload it on the proper circulation desk in Alma)
for key_lib, value in r_offline_circ.items():
    filedat = basename_datfile + user_alma_from.find("primary_id").text + "-to-" + user_alma_to.find("primary_id").text + "_" + key_lib + ".dat"
    offline_transfer = value + l_offline_circ.get(key_lib)
    with open(filedat, "w") as f:
        try:
            f.write("".join(offline_transfer))
        except:
            print("Error: file " + filedat + "not written.")
        f.close()
        print ("Creating file: " + filedat)
print ("\nDone: remember to upload the file/s in Alma'a offline circulation selecting first the appropriate library and circulation desk.")
    
