import boto3
import requests
import os
import smtplib
import paramiko
import time

import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
instance_id = "i-0c90f5640105608c3"
host_ip = "13.234.116.18"


def send_notification(email_text):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_text)
        smtp.close()
        print("Email sent successfully!")


def restart_application():
    print("restart_application")
    key = "C:/Users/Himanshu/Downloads/Documents/aws_stuff/vprofile_ap_s1.pem"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=host_ip,
            username="ubuntu",
            key_filename=key
        )
        stdin, stdout, stderr = client.exec_command("docker start fdcaf261ffbb")
        print(stdout.readlines())
        client.close()
    except Exception as exc:
        print(exc)


def restart_server_and_container():
    # restart ec2 server
    ec2_client = boto3.client('ec2')
    print("Restarting the server...")
    ec2_client.reboot_instances(
        InstanceIds=[
            instance_id
        ]
    )

    # restart the application
    print("Restarting the container...")
    time.sleep(60)
    restart_application()


def monitor_website():
    try:
        response = requests.get('http://ec2-13-234-116-18.ap-south-1.compute.amazonaws.com:8080/')

        if response.status_code == 200:
            print("Application is UP and RUNNING!")
        else:
            print("Application DOWN, need to be FIXED!")
            msg = f"""Subject: SITE DOWN\n
            Application Response Code: {response.status_code}."""
            send_notification(msg)

            # restart the application
            restart_application()

    except Exception as ex:
        print(f"==========CONNECTION_ERROR==============\n{ex}")
        msg = "Subject: CONNECTION ERROR\nApplication is not Reachable!"
        send_notification(msg)
        restart_server_and_container()


schedule.every(15).minutes.do(monitor_website)

while True:
    schedule.run_pending()
