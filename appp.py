import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Wikipedia Yearly Events", layout="centered")

st.title("📅 Wikipedia Events Finder by Year")
st.write("Enter a year to find out what major events happened that year!")

year = st.text_input("Enter Year (e.g., 1991)", max_chars=4)

def get_wikipedia_events(year):
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": year,
        "format": "json",
        "prop": "text",
        "redirects": True
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    if "parse" not in data:
        return None

    soup = BeautifulSoup(data["parse"]["text"]["*"], 'html.parser')
    
    events_header = soup.find(id="Events")
    if not events_header:
        return None

    events_list = []
    for tag in events_header.parent.find_next_siblings():
        if tag.name == "h2":
            break
        if tag.name == "ul":
            for li in tag.find_all("li"):
                text = li.get_text().strip()
                if text:
                    events_list.append(text)
        if len(events_list) >= 50:
            break  # Stop after collecting 50 events
    return events_list[:50]  # Only return top 50

if year:
    if year.isdigit() and 1000 <= int(year) <= 2099:
        st.info(f"Searching for events in {year}...")
        events = get_wikipedia_events(year)
        if events:
            st.success(f"Showing Top {len(events)} Events in {year}")
            for i, event in enumerate(events, 1):
                st.markdown(f"**{i}.** {event}")
        else:
            st.warning("No events found or Wikipedia page format is different.")
    else:
        st.error("Please enter a valid 4-digit year between 1000 and 2099.")
