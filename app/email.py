import smtplib
my_email = 'kodiugos@gmail.com' #email
pwd = 'llhytkakbfhnikci'#password

def send_email(to, subject, confirm_url):
    # Send verification email
    with smtplib.SMTP('smtp.gmail.com') as connection:
        # secure connection
        connection.starttls()
        # login to email
        connection.login(user=my_email, password=pwd)
        # send an email
        connection.sendmail(from_addr=my_email,
                            to_addrs=to,
                            msg=f'Subject:{subject}\n\n Url:{confirm_url}')
    print('sent email')
