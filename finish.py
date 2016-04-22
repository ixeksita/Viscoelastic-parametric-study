#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
#This code is used to email the  satatus of the FEA simulation 

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
 
fromaddr = *******
toaddr =  ***************
password=  **************

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "ABAQUS simulations status"
 
body = "Simulations complete!!! Check the results and output files"
msg.attach(MIMEText(body, 'plain'))

#NOTE: filename should be the path to the file, since the entire automated script operates on the work directory
# this specific line do not require referencing to the path

filename = "simulations_status.txt"
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)
 
#note that in gmail you need to have accepted access from less secure sources 
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(fromaddr, password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()