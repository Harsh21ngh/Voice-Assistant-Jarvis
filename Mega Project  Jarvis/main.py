import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = "70f071f79b1144b0b7ac01801e48a6ce"
openai_api_key = "your_openai_api_key_here"
openai.api_key = openai_api_key

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.co.in/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open bing" in c.lower():
        webbrowser.open("https://www.bing.com/?FORM=Z9FD1")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open chat gpt" in c.lower():
        webbrowser.open("https://chat.openai.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/feed/?trk=guest_homepage-basic_google-one-tap-submit")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[-1].strip()
        link = musicLibrary.musicLibrary.get(song)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Sorry, I couldn't find that song.")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if articles:
                for article in articles[:5]:  # Limit to 5 articles
                    speak(article.get("title", "No title available"))
            else:
                speak("Sorry, no news articles found.")
        else:
            speak("Unable to fetch news at the moment.")

    elif "question" in c.lower():
        question = c.lower().replace("question", "").strip()
        if question:
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=question,
                    max_tokens=50,  # Limit the response length for short and to-the-point answers
                    temperature=0.7
                )
                answer = response.choices[0].text.strip()
                speak(answer)
            except Exception as e:
                speak("Sorry, I couldn't process your question.")
                print(f"Error with OpenAI API: {e}")
        else:
            speak("Please ask a valid question.")

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Hey")

                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")
