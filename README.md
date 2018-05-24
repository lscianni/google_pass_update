## google_pass_update

AutoPassUpdate.py

Update google directory user's passwords from a csv file. 

Uses the google client api.

Creates a log of updated passwords and responses from the google server. The loggs are saved in the google_pass_update directory and saved to  'passwordupdate.log'. 

#### Required Modules
google-api-python-client

#### Usage 

Place a properly formatted CSV file in AutoPassUpdate working directory and run the script.

#### CSV file format

~~~
SamAccountName,Password
username,newpassword
~~~

