import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import requests
import yfinance as yf
import translators as ts
import time
import wikipedia
import datetime

apple = yf.Ticker('AAPL')
tesla = yf.Ticker('TSLA')
microsoft = yf.Ticker('MSFT')



news_api_key = 'key'

weather_api_key = 'key'

# Entfernungs-api-key
distance_api_key = 'key'

# Weekday Today
weekday_today = datetime.datetime.now().strftime("%A")


def translator(text):
    neptun_talk_en(ts.google(text, from_language='de', to_language='en'))


def get_news():
    news = 'https://newsapi.org/v2/top-headlines?country=de&category=buisness&apiKey=' + news_api_key

    news_json = requests.get(news).json()
    articles = news_json['articles']

    news_headlines = []
    for x in articles:
        news_headlines.append(x['title'])

    for i in range(3):
        print(news_headlines[i])
        neptun_talk(news_headlines[i])


def get_weather():
    neptun_talk('Kein Problem, für welche Stadt soll ich das Wetter nachsehen?')
    weather_input = neptun_listen()

    weather_url = 'https://api.weatherbit.io/v2.0/current?city=' + weather_input + '&key=' + weather_api_key
    weather_json = requests.get(weather_url).json()
    # weather_json

    temperature = weather_json['data'][0]['temp']
    print(temperature)
    neptun_talk('Die Temperatur in ' + weather_input + 'beträgt ' + str(temperature) + ' Grad.')


def distance_info():
    neptun_talk('Klar, was ist der Startpunkt?')

    location_one = neptun_listen()
    print(location_one)
    time.sleep(1)
    neptun_talk('Okay, und der Endpunkt?')
    location_two = neptun_listen()
    print(location_two)
    neptun_talk('Gib mir einen Moment. Ich benutze mein schlaues Köpfchen um es für dich zu berechnen')

    dist_url = 'www.mapquestapi.com/directions/v2/route?key=meinKey&from=' + location_one
    '&to=' + location_two + '&unit=k'
    dist_request = requests.get(dist_url).json()
    distance_km = round(dist_request['route']['distance'], 2)
    distance_result = 'Die Entfernung zwischen ' + location_one + ' und ' + location_two + ' beträgt ' + str(
        distance_km) + 'Kilometer.'
    print(distance_result)
    neptun_talk(distance_result)


def wikipedia_info():
    neptun_talk('Ich schaue gerne für dich nach. Wonach soll ich suchen?')
    wikipedia.set_lang('de')
    wiki_listen = neptun_listen()
    wiki_result = wikipedia.summary(wiki_listen, sentences=1)
    print(wiki_result)
    neptun_talk(wiki_result)


def get_time_now():
    today_date = datetime.datetime.now()
    hour = today_date.strftime("%H")
    minute = today_date.strftime("%M")
    time_now = 'Es ist ' + hour + ':' + minute
    print(time_now)
    neptun_talk(time_now)


def weekday_german(weekday_today):
    if 'monday' in weekday_today.lower():
        return 'montag'
    elif 'tuesday' in weekday_today.lower():
        return 'dienstag'
    elif 'wednesday' in weekday_today.lower():
        return 'mittwoch'
    elif 'thursday' in weekday_today.lower():
        return 'donnerstag'
    elif 'friday' in weekday_today.lower():
        return 'freitag'
    elif 'saturday' in weekday_today.lower():
        return 'samstag'
    else:
        return 'sonntag'


# sprache zu text konvertieren - sodasss wir den text im nächsten Schritt verwenden können
def neptun_listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        audio = r.listen(source)
        text = ''

        try:
            text = r.recognize_google(audio, language='de-DE')
        except sr.RequestError as re:
            print(re)
        except sr.UnknownValueError as uve:
            print(uve)
        except sr.WaitTimeoutError as wte:
            print(wte)

    text = text.lower()
    return text


# text zu sprache konvertieren - sodass der übergebene Text im audioformat ausgegeben werden kann
def neptun_talk(text):
    # erzeuge audio Datei
    file_name = 'C:/Users/Administrator/audio.mp3'
    # konvertiere text zu sprachen
    tts = gTTS(text=text, lang='de')
    # speichern
    tts.save(file_name)
    # abspielen
    playsound.playsound(file_name)
    # löschen
    os.remove(file_name)


# englisch
def neptun_talk_en(text):
    # erzeuge audio Datei
    file_name = 'C:/Users/Administrator/audio.mp3'
    #konvertiere text zu sprachen
    tts = gTTS(text=text, lang='en')
    # speichern
    tts.save(file_name)
    # abspielen
    playsound.playsound(file_name)
    # löschen
    os.remove(file_name)


def neptun_reply(text):
    # Smalltalk - wie ist dein Name?
    if 'wie' in text and 'name' in text:
        neptun_talk('Ich bin die Emelina und bin deine persönliche Sprachassistentin.')

    elif 'warum' in text and 'existierst' in text:
        neptun_talk('Ich wurde geschaffen um für dich zu arbeiten. Ich brauche keine Pausen und keine Auszeit.')

    elif 'wann' in text and 'schläfst' in text:
        neptun_talk('Ich schlafe nie. Ich arbeite 24 Stunden.')

    elif 'bist' in text and 'dumm' in text:
        neptun_talk('Nein, ich bin nicht dumm. Meine Oma hat gesagt, dass es keine dummen Menschen gibt.'
                     + 'Ich gebe mein bestes, um jeden Tag etwas neues zu lernen.')

    elif 'film' in text or 'lieblingstext' in text:
        neptun_talk('Ich schaue am liebsten Titanic. Ich habe ihn mir bestimmt schon mehr als 20 mal angesehen.')



    elif 'apple' in text:
        apple_stock_price = apple.info['open']
        neptun_talk('Zu diesem Zeitpunkt kannst du eine Aktie von Apple für ' + str(apple_stock_price).replace('.',
                                                                                                                ',') + ' US Dollar kaufen.')

    elif 'tesla' in text:
        tesla_stock_price = tesla.info['open']
        neptun_talk('Zu diesem Zeitpunkt kannst du eine Aktie von Tesla für ' + str(tesla_stock_price).replace('.',
                                                                                                                ',') + ' US Dollar kaufen.')

    elif 'microsoft' in text:
        microsoft_stock_price = microsoft.info['open']
        neptun_talk(
            'Zu diesem Zeitpunkt kannst du eine Aktie von Microsoft für ' + str(microsoft_stock_price).replace('.',
                                                                                                               ',') + ' US Dollar kaufen.')

    # Übersetzer von Deutsch in Englisch
    elif 'uebersetzen' in text or 'uebersetzer' in text:
        neptun_talk('Klar, sag mir einfach was ich übersetzen soll.')

        while True:
            text_to_translate = neptun_listen()
            print(text_to_translate)

            if text_to_translate == 'übersetzer ausschalten':
                translator(text_to_translate)

            else:
                neptun_talk('Ich habe den Übersetzer ausgeschaltet. Kann ich sonst noch etwas für dich tun?')
                break



    # News
    elif 'news' in text or 'nachrichten' in text:
        neptun_talk('Kein Problem hier sind die Top 3 Nachrichten von heute')
        get_news()

    # Wetter
    elif 'wetter' in text:
        get_weather()


    # Entfernung
    elif 'distanz' in text or 'entfernung' in text:
        distance_info()

    # Wikipedia
    elif 'wikipedia' in text:
        wikipedia_info()

    # Uhrzeit
    elif 'wie' in text and 'spät' in text:
        get_time_now()


    # Wochentag
    elif 'wochentag' in text:
        neptun_talk('Heute ist ' + weekday_german(weekday_today))


    elif 'stop' in text or 'stopp' in text:
        neptun_talk('Es war mir eine Freude dir zu helfen. Ich wünsche dir einen schönen Tag.')

    else:
        neptun_talk('Entschuldige, ich habe dich nicht verstanden. Könntest du das bitte wiederholen?')