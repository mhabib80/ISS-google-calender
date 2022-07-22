from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from bs4 import BeautifulSoup
from datetime import timedelta
import requests
from dateutil import parser
import os

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
creds = Credentials.from_authorized_user_file('google_calendar_token.json', SCOPES)
service = build('calendar', 'v3', credentials=creds)


res = requests.get('https://spotthestation.nasa.gov/sightings/view.cfm?country=United_States&region=California&city=Orangevale#.YgGC2urMJaQ').content
soup = BeautifulSoup(res, 'html.parser')
rows = [row.find_all('td')[:5] for row in soup.find_all('tr')[1:]]

for r in rows:
    start = parser.parse(r[0].text)
    end = start + timedelta(minutes=4)
    desc = f'Appears {r[3].text}, Disappears {r[4].text}, Max ht= {r[2].text}'
    event = {
      'summary': 'ISS Sighting',
      'description': desc,
      'start': {
        'dateTime': start.isoformat(),
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': end.isoformat(),
        'timeZone': 'America/Los_Angeles',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'popup', 'minutes': 15},
        ],
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'''Event created: {event.get('htmlLink')}''')
