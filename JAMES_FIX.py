import json
import smtplib
from email.mime.text import MIMEText

def return_html_boiler(json_data):
    # Parse the JSON data
    data = json_data

    # Access data
    user1_email = data['id1']['email']
    user2_email = data['id2']['email']
    user1_name = data['id1']['name']
    user2_name = data['id2']['name']
    timeslots = data['timeslot']
    recipients = [user1_email, user2_email]

    # Generate timeslot HTML
    timeslot_html_parts = []
    for day, times in timeslots.items():
        times_formatted = ", ".join(times)
        timeslot_html_parts.append(f"<p><strong>{day}:</strong> {times_formatted}</p>")

    timeslots_html = "\n".join(timeslot_html_parts)

    # HTML string with placeholders
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ffd3c9; /* Light Peach */
            color: #333;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}

        .container {{
            width: 80%;
            max-width: 700px;
            margin: 20px auto;
            background: #fff;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}

        .header {{
            background-color: #ff9a9e; /* Soft Red */
            color: white;
            text-align: center;
            padding: 10px 0;
            border-radius: 8px 8px 0 0;
        }}

        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}

        .user-info {{
            display: flex;
            flex-direction: column; /* Stack the items vertically */
            align-items: center;
            padding: 20px 0;
        }}

        .user-info > div {{
            width: 100%; /* Full width for each player info */
            margin-bottom: 20px; /* Spacing between player info */
        }}

        .user-info h2 {{
            font-size: 18px;
            color: #ff9a9e; /* Soft Red */
            margin: 10px 0 5px 0;
        }}

        .user-info p {{
            font-size: 16px;
            margin: 5px 0;
        }}

        .timeslot-info {{
            background-color: #ffb5b0; /* Light Coral */
            padding: 15px;
            border-radius: 8px;
        }}

        .timeslot-info h2 {{
            color: #333;
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
            color: #333;
        }}

        a {{
            color: #ff9a9e; /* Soft Red */
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 600px) {{
            .user-info > div {{
                text-align: center;
            }}
        }}
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h1>Welcome to SquashNoFriends!</h1>
            </div>
            <div class='user-info'>
                <div>
                    <h2>Player 1</h2>
                    <p>
                        <strong>Name:</strong> {user1_name}
                    </p>
                    <p>
                        <strong>Email:</strong>
                        <a href="mailto:{user1_email}">{user1_email}</a>
                    </p>
                </div>
                <div>
                    <h2>Player 2</h2>
                    <p>
                        <strong>Name:</strong> {user2_name}
                    </p>
                    <p>
                        <strong>Email:</strong>
                        <a href="mailto:{user2_email}">{user2_email}</a>
                    </p>
                </div>
            </div>
            <div class='timeslot-info'>
                <h2>Common Available Timeslots</h2> {timeslots_html}
            </div>
        </div>
    </body>
    </html>
    """
    # Fill in the placeholders
    final_html = html_template.format(
        user1_name=user1_name,
        user1_email=user1_email,
        user2_name=user2_name,
        user2_email=user2_email,
        timeslots_html=timeslots_html)

    return final_html, recipients

def send_email(json_data):
    GMAIL_APP_PASSWORD = "jeco blgh eafn zotk"
    GMAIL_USERNAME = "squashnofriends"

    html_boiler, recipients = return_html_boiler(json_data)

    msg = MIMEText(html_boiler, 'html')
    msg["Subject"] = "Matched Players and All Times"
    msg["To"] = ", ".join(recipients)
    msg["From"] = f"{GMAIL_USERNAME}@gmail.com"

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
        smtp_server.sendmail(msg["From"], recipients, msg.as_string())
        smtp_server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# # Example usage
# json_data = {
#     'id1': {'email': 'jamesk@gmail.com', 'name': 'james'},
#     'id2': {'email': 'email2@example.com', 'name': 'Name2'},
#     'timeslot': {'Monday': ['9 AM - 10 AM', '1 PM - 2 PM']}
# }
# send_email(json_data)
