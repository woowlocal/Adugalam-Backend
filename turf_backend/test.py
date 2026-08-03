import requests
from bs4 import BeautifulSoup
try:
    r = requests.post('http://127.0.0.1:8000/api/admin/events/', data={'eventName': 'Test'})
    if r.status_code == 500:
        soup = BeautifulSoup(r.text, 'html.parser')
        # Django's error page has a div with class 'exception_value' and the traceback in 'traceback'
        print(soup.title.text)
        frames = soup.find_all('li', class_='frame')
        if frames:
            last_frame = frames[-1]
            print(last_frame.text.strip())
        print(soup.find('div', class_='exception_value').text if soup.find('div', class_='exception_value') else 'No exception value')
except Exception as e:
    print(e)
