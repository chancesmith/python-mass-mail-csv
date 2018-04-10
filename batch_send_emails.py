import csv
import os
import sys
from time import sleep
from send_email import send_email as sendDatEmail
from env import csvFile, gifPath

# vars
sentCount = 0
noEmailCount = 0
errorCount = 0
leftToSendCount = 0
sentOne = False

with open(csvFile) as csv_in_file:
    reader = csv.reader(csv_in_file)
    with open('data-temp.csv', 'w') as csv_out_file:
        writer = csv.writer(csv_out_file)
        # add every preexisting row in CSV before adding another
        for row in reader:
            hasBeenSent = str(row[10])
            gif = gifPath+row[9]
            email = str(row[4])
            firstName = str(row[2]).capitalize()
            # lastName = str(row[3])

            # skip first row
            if row[9] == 'Gif':
                writer.writerow(row)
                continue
            # only send one email per instance
            if sentCount == 5:
                if hasBeenSent:
                    leftToSendCount += 1
                writer.writerow(row)
                continue
            # if email is empty or invalid, move on
            if email == '':
                # errorCount += 1
                noEmailCount += 1
                # print('empty email')
                row[10] = 'True'
                writer.writerow(row)
                continue
            elif '@' not in email:
                # errorCount += 1
                print('email not valid with @')
                row[10] = 'True'
                writer.writerow(row)
                continue
            # don't sent if already sent
            if hasBeenSent == 'True':
                # print('Already sent')
                writer.writerow(row)
                continue
            else:
                leftToSendCount += 1
            # if has not been sent, send email
            sent = sendDatEmail(firstName, email, gif)
            # print('Sent var = '+str(sent))
            if sent is True:
                # print('Email sent')
                sentCount += 1
                leftToSendCount -= 1
                row[10] = 'True'
                # print('Ends: '+str(row[10]))
                writer.writerow(row)
                sentOne = True
                continue
            else:
                print('Email did not send: '+email)
                errorCount += 1
                writer.writerow(row)
                continue
    os.rename('data-temp.csv', csvFile)

print('CSV run through and updated.')
print('Emails sent: '+str(sentCount))
print('Emails not found: '+str(noEmailCount))
print('Email errors: '+str(errorCount))
print('Email left to send: '+str(leftToSendCount))
