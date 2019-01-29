# Alma-LoanTransfer
Bulk transfer loans from a user to another user with Alma Offline circulation

Create one or more .dat files to upload in Alma Offline Circulation tool [2]

* check if both users id exist in Alma
* check if user_from has loans
* create a .dat file for every loans libraries and circulation desks
* every .dat file perfom items returns from user from and loans to user_to, at the same date and time of initial loan (plus one minute for return and two minutes for reloan)
* if loans are renewed a event error is possible trying to upload in offline circulation: since there is no possibility to obtain the last renew date the script can set the return/reloan date n days prior due date
* date and time in UTC format are automatically adjusted on the local time

## Usage
command: 
```
python loantransfer.py [user_id_from] [user_id_to]
python loantransfer.py [user_id_from] [user_id_to] -d 30
```
In Alma Circulation tool upload the .dat file/s selecting previously the correct library/circulation desk.

## Installation
No installation needed, simply download loantransfer.py in a rw directory.
In the ini-section add your institution Alma user API key and API server baseurl [3].

## Prerequisites
* Python v3 with modules: requests, time, datetime, xml.etree, argparse 
* Alma Ex Libris
* User API access and key

## Authors
* **Nazzareno Bedini - University of Pisa**

## Acknowledgments
* \[1\] [Alma Bulk Loan Transfer Using Analytics and Offline Circ](https://developers.exlibrisgroup.com/blog/Alma-Bulk-Loan-Transfer-Using-Analytics-and-Offline-Circ) - the script is inspired by this Alma developers tech blog post;
* \[2\] [Offline Circulation ](https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/030Fulfillment/070Advanced_Tools/060Offline_Circulation);
* \[3\] [General info to start to works with Alma's APIs](https://developers.exlibrisgroup.com/alma/apis) - HowTo obtain the API key for your environment.
