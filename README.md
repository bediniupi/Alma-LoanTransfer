# Alma-LoanTransfer
Bulk transfer loans from a user to another user with Alma Offline circulation
Create one or more .dat files to upload in Alma Offline Circulation tool [2]

* check if both users id exist in Alma
* check if user_from has loans
* create a .dat file for every loans libraries and circulation desks
* every .dat file perfom items returns from user from and loans to user_to, at the same date and time of initial loan (plus one minute for return and two minutes for reloan) (note: possibly event error in case of renew)
* date and time in UTC format are adjusted on the local time

## Usage
command: 
```
python loantransfer.py [user_id_from] [user_id_to]
```
In Alma Circulation tool upload the .dat file/s selecting previously the correct library/circulation desk.

## Installation
No installation needed, simply download loantransfer.py in a rw directory.
In the ini-section add your institution Alma api key and api server baseurl [3].

## Prerequisites
Python v 2.7, modules requests, time, datetime, xml.etree 
Alma Ex Libris 

## Authors
* **Nazzareno Bedini - University of Pisa**

## Acknowledgments
* \[1\] [Alma Bulk Loan Transfer Using Analytics and Offline Circ](https://developers.exlibrisgroup.com/blog/Alma-Bulk-Loan-Transfer-Using-Analytics-and-Offline-Circ)
* \[2\] [Offline Circulation ](https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/030Fulfillment/070Advanced_Tools/060Offline_Circulation)
* \[3\] [General info to start to works with Alma's APIs](https://developers.exlibrisgroup.com/alma/apis) - HowTo obtain the API key to your environment
