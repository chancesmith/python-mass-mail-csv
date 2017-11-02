import csv
import os
import sys
from time import sleep
from send_email import send_email as sendDatEmail

sentCount = 0
errorCount = 0
sentOne = False

with open('data.csv') as csv_in_file:
    reader = csv.reader(csv_in_file)
    with open('data-temp.csv', 'w') as csv_out_file:
        writer = csv.writer(csv_out_file)
        # add every preexisting row in CSV before adding another
        for row in reader:
            # skip first row
            if row[9] == 'Gif':
                writer.writerow(row)
                continue
            # only send on email per instance
            if sentOne == True:
                writer.writerow(row)
                continue
            gif = 'files/'+row[9]
            email = str(row[4])
            firstName = str(row[2])
            lastName = str(row[3])
            hasBeenSent = str(row[10])
            # don't sent if already sent
            if hasBeenSent == 'True' :
                # print('Already sent')
                writer.writerow(row)
                continue
            # if has not been sent, send email
            sent = sendDatEmail(firstName, lastName, email, gif)
            # print('Sent var = '+str(sent))
            if sent is True:
                # print('Email sent')
                sentCount += 1
                row[10] = 'True'
                # print('Ends: '+str(row[10]))
                writer.writerow(row)
                # sentOne = True
                continue
            else:
                print('Email did not send: '+email)
                errorCount += 1
                writer.writerow(row)
                continue
    os.rename('data-temp.csv','data.csv')

print('CSV run through and updated.')
print('Emails sent: '+str(sentCount))
print('Email errors: '+str(errorCount))