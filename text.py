import os
import smtplib
from email.mime.text import MIMEText
import json

def create_json_data():
    data = [
        {
            "2": {
                "name": "Eric",
                "email": "ericfode2@gmail.com"
            },
            "9": {
                "name": "Sally",
                "email": "Sally@gmail.com"
            },
            "timeslot": {
                "Monday": ["09:00 AM", "10:00 AM"],
                "Tuesday": ["09:00 AM", "03:00 PM"],
                "Wednesday": ["09:00 AM", "10:00 AM"],
                "Thursday": ["01:00 PM", "07:00 PM"],
                "Friday": ["10:00 AM", "02:00 PM"],
                "Saturday": ["09:00 AM", "12:00 PM"],
                "Sunday": ["10:00 AM", "05:00 PM"]
            }
        },
        # ... (similar structures for other datasets)
    ]

    json_string = json.dumps(data, indent=4)
    with open("output.json", "w") as json_file:
        json_file.write(json_string)

def get_all_times(data):
    all_times = []
    day_times = {}

    for entry in data:
        if "timeslot" in entry:
            for day, timeslot in entry["timeslot"].items():
                if day not in day_times:
                    day_times[day] = []

                day_times[day].extend([(time, day) for time in timeslot])
                all_times.extend([(time, day) for time in timeslot])

    return all_times, day_times

def send_email():
    GMAIL_APP_PASSWORD = "jeco blgh eafn zotk"
    GMAIL_USERNAME = "squashnofriends"

    create_json_data()  # Call the function to create and save JSON data

    with open("output.json", "r") as json_file:
        data = json.load(json_file)

    recipients = set()
    player_names = []

    for entry in data:
        for key, value in entry.items():
            if key.isdigit() and "email" in value:
                recipients.add(value["email"])
                player_names.append(value["name"])

    if not recipients:
        print("No recipient emails found in the JSON data.")
        return

    all_times, day_times = get_all_times(data)

    # Build user information HTML
    user_info_html = ""
    for entry in data:
        for key, value in entry.items():
            if key.isdigit() and "email" in value:
                user_info_html += f"<p><strong>Name:</strong> {value['name']}</p>\n"
                user_info_html += f"<p><strong>Email:</strong> <a href='mailto:{value['email']}'>{value['email']}</a></p>\n"

    # Build timeslot information HTML
    timeslot_info_html = ""
    timeslot_info_html += "<h2>Common Available Timeslots</h2>\n"
    for day, timeslots in day_times.items():
        timeslot_info_html += f"<ul><strong>{day}:</strong> "
        for i, (time, day) in enumerate(timeslots):
            timeslot_info_html += f"<li><a href='https://recreation.mcgill.ca/booking-help'>{time}</a></li>"
            if day == "Sunday" and i == len(timeslots) - 1:
                timeslot_info_html += f"</ul>\n<p>For more information on how to book, please check the <a href='https://recreation.mcgill.ca/booking-help'>schedule</a>.</p>\n"
            elif i == len(timeslots) - 1:
                timeslot_info_html += "</ul>\n"
            else:
                timeslot_info_html += " "

    # Include player names and all times in the body of the email
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Matched Timeslot Information</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                width: 80%;
                margin: auto;
                background: #fff;
                padding: 20px;
            }}
            .header {{
                background: #333;
                color: #fff;
                padding: 10px 0;
                text-align: center;
            }}
            .user-info, .timeslot-info {{
                margin: 20px 0;
            }}
            .timeslot-info h2 {{
                color: #ffb5b0; /* Light Coral */
                margin-top: 0;
            }}
            .timeslot-info ul {{
                list-style-type: none;
                padding: 0;
            }}
            .timeslot-info li {{
                background-color: #ffc1b6; /* Peach */
                margin: 10px 0;
                padding: 10px;
                border-left: 4px solid #ffcabf; /* Soft Peach */
            }}
            .timeslot-info li strong {{
                color: #ffcabf; /* Soft Peach */
            }}
            .footer {{
                background-color: #ffd3c9; /* Light Peach */
                color: #333333;
                text-align: center;
                padding: 10px 0;
                font-size: 14px;
            }}
            .footer p {{
                margin: 0;
            }}
            a {{
                color: #ff9a9e; /* Soft Red */
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Matched Timeslot Details</h1>
            </div>

            <!-- User Information -->
            <div class="user-info">
                <h2>User Details</h2>
                {user_info_html}
            </div>

            <!-- Timeslot Information -->
            <div class="timeslot-info">
                {timeslot_info_html}
            </div>

            <div class="footer">
                <p>Thank you for using our service!</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Print the emails, player names, and all times to the console
    print("Sending email to:", ", ".join(recipients))
    print("Matched players:", ", ".join(player_names))
    print("All Times:", ", ".join(f'{time} ({day})' for time, day in all_times))

    msg = MIMEText(email_body, 'html')

    msg["Subject"] = "Matched Players and All Times"
    msg["To"] = ", ".join(recipients)
    msg["From"] = f"{GMAIL_USERNAME}@gmail.com"

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
    smtp_server.sendmail(msg["From"], recipients, msg.as_string())
    smtp_server.quit()

if __name__ == "__main__":
    send_email()
