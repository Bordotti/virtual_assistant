#Importing Libraries
import speech_recognition as sr
import pyttsx3
# import pywhatkit
import datetime
# import wikipedia
# import pyjokes
import requests, json , sys
# import schedule
#PyAudio
#PyWhatKit
#PyJokes
#Wikipedia
#OpenweatherApi

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 230)
lembretes = []

def engine_talk(text):
    engine.say(text)
    engine.runAndWait()
   
def user_commands():
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source)
            print('analisando voz')
            command = listener.recognize_google(voice, language='pt-BR')
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print(command)
                engine_talk('How can i help you?')
                command = None
                while command is None:
                    print("Aguardando comando")
                    voice = listener.listen(source)
                    print('analisando voz')
                    command = listener.recognize_google(voice, language='pt-BR')
                    command = command.lower()

                return command
    except:
        pass
    
def avisa_lembretes():
    tol_antes = datetime.datetime.now()-datetime.timedelta(minutes=5)
    tol_depois = datetime.datetime.now()+datetime.timedelta(minutes=5)
    to_remove = []
    for e, lembrete in enumerate(lembretes):
        if tol_antes <  lembrete['hora'] < tol_depois:
            engine_talk('Lembrete, Lembrete. ' + lembrete['nota'])
            with sr.Microphone() as source:
                engine_talk('Deseja adiar o lembrete?')
                voice = listener.listen(source)
                command = listener.recognize_google(voice, language='pt-BR')
                command = command.lower()
                if command is not None:
                    resp = adia_lembrete(command)
                    if resp == -1: to_remove.append(e)
                    else: lembrete['hora'] = resp
                    print(resp)
                

def adia_lembrete(command):
    try:
        if 'sim' in command:
            return datetime.datetime.now()+datetime.timedelta(minutes=10)
        elif 'adiar' in command:
            if 'minutos' in command:
                command = command.replace('adiar', '').replace('minutos', '').strip()
                minutes = int(command)
                return datetime.datetime.now()+datetime.timedelta(minutes=minutes)
            elif 'hora' in command:
                command = command.replace('adiar', '').replace('hora', '').replace('horas', '').strip()
                hora = int(command)
                return datetime.datetime.now()+datetime.timedelta(hours=hora)
        elif 'não' in command:
            return -1
    except Exception as e:
        print(e)
        engine_talk(f'Não foi possível adiar o lembrete, {e}')
    

def run_jarvis():
    command = None
    while command is None:
        command = user_commands()
    if 'tocar' in command:
        song = command.replace('tocar', '')
        #print('New Command is' +command)
        #print('The bot is telling us: Playing' +command)
        engine_talk('Playing' +song)
        pywhatkit.playonyt(song)
    elif 'lembrete' in command:
        print(command)
        command = command.lstrip('adicionar um lembrete às ')
        hora = command[:6].strip()
        nota = command[6:] 
        # command = command.lstrip('adicionar').lstrip('um').lstrip('lembrete').lstrip('às').split('nota')
        print(command,'|', hora, '|', nota)
        hora = datetime.datetime.strptime(hora, '%H:%M')
        
        lembretes.append({'nota':nota, 'hora':hora})
        print(f"Lembrete adicionado: {nota=}, {hora=}")

    # elif 'time' in command:
    #     time = datetime.datetime.now().strftime('%I:%M %p')
    #     engine_talk('The current time is' +time)
    # elif 'who is' in command:
    #     name = command.replace('who is' , '')
    #     info =  wikipedia.summary(name, 1)
    #     print(info)
    #     engine_talk(info)
    # elif 'joke' in command:
    #     engine_talk(pyjokes.get_joke())
    # elif 'weather' in command:
    #     engine_talk('Please tell the name of the city')
    #     city = user_commands()
    #     #weather_api = weather('Hong Kong')
    #     weather_api = weather(city)
    #     engine_talk(weather_api + 'degree fahreneit' )
    elif 'parar' in command:
        sys.exit()
    else:
        engine_talk('I could not hear you properly')


 
def weather(city):
    # Enter your API key here 
    api_key = "2f192ed601337bc46cf188b08f6e189e"
    
    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name 
    city_name = city
    
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
    
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json() 
    
    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 
    
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
    
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 
    
        # store the value corresponding 
        # to the "pressure" key of y 
        #current_pressure = y["pressure"] 
    
        # store the value corresponding 
        # to the "humidity" key of y 
        #current_humidiy = y["humidity"] 
    
        # store the value of "weather" 
        # key in variable z 
        #z = x["weather"] 
    
        # store the value corresponding  
        # to the "description" key at  
        # the 0th index of z 
        #weather_description = z[0]["description"]
        return str(current_temperature)
    
        # print following values 
        '''print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) + 
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidiy) +
            "\n description = " +
                        str(weather_description)) 
    else: 
        print(" City Not Found ")
        '''


        
while True:
    run_jarvis()
    avisa_lembretes()
    