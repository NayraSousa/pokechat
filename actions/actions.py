# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from type_pokemon import get_types
from ability_pokemon import get_ability
from move_pokemon import get_moves

from random import choice
import spacy
import requests
from LeIA import SentimentIntensityAnalyzer

from statistics_pokemon import get_statistics
from image_pokemon import get_image

nlp = spacy.load("pt_core_news_md")
sentiment_analyser = SentimentIntensityAnalyzer()

user_pokemon = None
user_sentiment = None
response = None

def default_low_trust_message(tracker, dispatcher):
    confidence = tracker.get_last_event_for("user")["parse_data"]["intent"]["confidence"]

    if confidence < 0.8:
        dispatcher.utter_message(text=choice([
            "Perdão, acho que não entendi sua mensagem.",
            "Desculpe-me, o que você quis dizer com isso?",
            "Perdão, acho que não fui programado para entender isso."
        ]))
        return True
    else:
        return False

class ActionRespostaHumorPerguntaPokemon(Action):

    def name(self) -> Text:
        return "action_resposta_humor_pergunta_pokemon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if default_low_trust_message(tracker, dispatcher):
            return []
    
        response_sentiment = sentiment_analyser.polarity_scores(tracker.latest_message['text'])

        global user_sentiment
        user_sentiment = response_sentiment

        if response_sentiment['pos'] > response_sentiment['neg'] or response_sentiment['neu'] > response_sentiment['neg']:
            dispatcher.utter_message(text="Que ótimo! Me diga, qual seu pokemon favorito?")
        else:
            dispatcher.utter_message(text="Poxa... Ao menos me diga seu pokemon favorito para alegrar seu dia :/")
    
        return []

class ActionDefinePokemonExibeSumario(Action):

    def name(self) -> Text:
        return "action_define_pokemon_exibe_sumario"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if default_low_trust_message(tracker, dispatcher):
            return []
        
        buttons = [
            {"title": "Estatísticas", "payload": "Estatísticas"},
            {"title": "Tipos", "payload": "Tipos"},
            {"title": "Imagem", "payload": "Imagem"},
            {"title": "Habilidades", "payload": "Habilidades"},
            {"title": "Movimentos", "payload": "Movimentos"},
        ]

        if tracker.get_slot('pokemon_slot'):
            global user_pokemon
            global user_sentiment
            global response
            user_pokemon = tracker.get_slot('pokemon_slot')
            response = requests.get(url=f"https://pokeapi.co/api/v2/pokemon/{user_pokemon}/")

            if response.status_code == 404:
                dispatcher.utter_message(text="Desculpa! Não consegui localizar esse pokemon.")

            elif response.status_code == 200:
                
                if user_sentiment['pos'] > user_sentiment['neg'] or user_sentiment['neu'] > user_sentiment['neg']:
                    dispatcher.utter_message(text="Qual informação você quer acessar?", buttons=buttons)
                else:
                    dispatcher.utter_message(text="Certo, ao menos corra atrás dos seus sonhos e não deixe ninguém pará-lo!. Aproveite e escolha uma dessas opções:", buttons=buttons)

            else:
                dispatcher.utter_message(text="Erro inesperado")

        else:
            dispatcher.utter_message(text="Perdão, não entendi seu pokemon preferido...")

        return []
   
class ActionGenerica(Action):

    def name(self) -> Text:
        return "action_generica"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if default_low_trust_message(tracker, dispatcher):
            return []

        user_choice = tracker.latest_message['text']

        if user_pokemon:
            if user_choice == "Estatísticas":
                dispatcher.utter_message(text=get_statistics(response.json()))
            elif user_choice == "Tipos":
                dispatcher.utter_message(text=get_types(response.json()))
            elif user_choice == "Imagem":
                dispatcher.utter_message(text="Confira a imagem do pokemon: ", image=get_image(response.json()))
            elif user_choice == "Habilidades":
                dispatcher.utter_message(text=get_ability(response.json()))
            elif user_choice == "Movimentos":
                dispatcher.utter_message(text=get_moves(response.json()))
            else:
                dispatcher.utter_message(text="Perdão, não entendi sua escolha")
        else:
            dispatcher.utter_message("Perdão, você não me disse seu pokemon favorito")
    
        return [SlotSet("pokemon_slot", None)]