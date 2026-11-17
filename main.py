# Project intended take your speech and open up the relevant wikipedia page
# Step 1. Record speech
# Step 2. Turn speech into a readable format e.g. string
# Step 3. Open up the relevant wikipedia page

# Speech recognition is not perfect, e.g. Black Myth: Wukong is the correct wikipedia page
# however it may return "black myth wukong" instead resulting in no page returning.
# Step 4. Identify if the string "Wikipedia does not have an article with this exact name." exists within the page.
# If so, return the search page for wikipedia.

import speech_recognition as sr
import webbrowser
import requests

r = sr.Recognizer()
notfound = "Wikipedia does not have an article with this exact name."
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

while True:
    try:
        with sr.Microphone() as source:
            print("Awaiting speech input...")

            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()

            # Debugging purposes
            # print(f"Speech detected: {text}")

            if text.startswith("wiki"):
                print("Opening Wikipedia query...")
                # search_query = text.replace("wiki", "") What if the user wants to search wikipedia about wikipedia.
                # It will replace wikipedia with pedia which isn't useful
                search_query = text[5:] # Slice the string to start from pos 5 which removes "wiki "
                print(f"Search query detected: {search_query}")

                # url = f"https://en.wikipedia.org/wiki/{search_query}"
                # This works, however using https://en.wikipedia.org/w/index.php?search= seems to find pages
                # that are simlar/close to the query rather than an exact match
                url = f"https://en.wikipedia.org/w/index.php?search={search_query}"

                # Check the wikipedia page exists first.
                res = requests.get(url, headers=headers)

                # For use in debugging to see what is being returned.
                # with open("res.txt", "w") as f:
                #     f.write(res.text)
                #     print("Wrote res.txt")

                # Check if the notfound text exists in request body, if so, open the search page for wikipedia
                if notfound in res.text:
                    print("Sorry, couldn't find anything, please see wikipedia search.")
                    search_url = f"https://en.wikipedia.org/w/index.php?search={search_query}&title=Special%3ASearch&fulltext=1&ns0=1"
                    webbrowser.open(search_url)

                # Otherwise, open the correct page.
                else:
                    webbrowser.open(url)

            if text.startswith("exit"):
                print("Goodbye - \"Exit\" keyword detected")
                break

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except KeyboardInterrupt:
        print("Goodbye - Program ended")
        break