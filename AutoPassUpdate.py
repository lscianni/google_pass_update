#!/usr/bin/env python3
#
# Update google directory passwords 
# From csv file
#
# Louis Scianni
# Released under GPL-v2

import httplib2, os, csv
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'AutoPassUpdate'

file_name = 'test.csv' # change this to the name of the real csv file
email_suffix = '@appliedtechres.com'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'admin-directory_v1-AutoPassUpdate.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)
    log_file = 'passwdupdate.log'

    data = {} # create an empty Dict for json
    with open(file_name) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader: # loop through csv file
            print('Reading CSV file')
            username = row['SamAccountName'] # parse usernames
            passwd = row['Password'] # parse passwords
            f = open(log_file, 'a')
            f.write(username + '\n')
            data['password'] = passwd # set the value as the password from the csv file
            #json_obj = json.dumps(data) # dump data into json format
            email = '%s%s' % (username, email_suffix)
            print('Updating %s password' % username)
            results = service.users().update(userKey=email, body=data ).execute() # API call 
            f.write(str(results) + '\n') # print the results
            f.close()
if __name__ == '__main__':
    main()
