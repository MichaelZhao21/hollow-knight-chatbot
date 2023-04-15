# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from Levenshtein import distance
import re
import json
import os
import urllib.parse


def read_kb():
    """Read the knowledge base from the output-kb directory"""
    pattern = re.compile('[\W_]+', re.UNICODE)

    # Read knowledge base
    kb = dict()
    topics = list()

    for filename in os.listdir('output-kb'):
        with open('output-kb/' + filename, 'r') as file:
            key = pattern.sub('', urllib.parse.unquote(
                filename.replace('_(Hollow_Knight)', ''))).lower()
            kb[key] = json.load(file)
            topics.append(key)

    return kb, topics


# Load the knowledge base
# This is loaded globally so that it is only loaded once
# and not every time the action is called
kb, topics = read_kb()


def min_dist(word: str, vec: list[str]):
    """Find the closest word (in Levenshtein Distance) to the given input word from a list of words"""
    min = 2**32 - 1
    min_word = ""
    for v in vec:
        d = distance(word, v)
        if d < min:
            min = d
            min_word = v
    return min_word, min


def get_topic(topic: str):
    """Find the closest topic to the given input topic from Rasa"""
    if topic in kb:
        return topic
    else:
        min_word, _ = min_dist(topic, topics)
        return min_word


def get_response_from_dict(topic, intent):
    """Get a response from the knowledge base if it exists, otherwise return a default response"""
    if intent not in kb[topic]:
        return "I'm sorry, I can't answer that question."
    return kb[topic][intent]


class ActionGetInfo(Action):
    """Get information about a topic from the knowledge base"""
    def name(self) -> Text:
        return "action_get_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = get_topic(topic)
        res = get_response_from_dict(topic, "info")
        dispatcher.utter_message(text=res)
        return []


class ActionGetBehavior(Action):
    """Get the behavior of a topic from the knowledge base"""
    def name(self) -> Text:
        return "action_get_behavior"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = get_topic(topic)
        res = get_response_from_dict(topic, "behavior")
        dispatcher.utter_message(text=res)
        return []


class ActionGetTrivia(Action):
    """Get trivia about a topic from the knowledge base"""
    def name(self) -> Text:
        return "action_get_trivia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = get_topic(topic)
        res = get_response_from_dict(topic, "trivia")
        dispatcher.utter_message(text=res)
        return []


class ActionGetJournal(Action):
    """Get the journal entry for a topic from the knowledge base"""
    def name(self) -> Text:
        return "action_get_journal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = get_topic(topic)
        res = get_response_from_dict(topic, "journal_entry")
        dispatcher.utter_message(text=res)
        return []


class ActionGetLocation(Action):
    """Get the location of a topic from the knowledge base"""
    def name(self) -> Text:
        return "action_get_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = get_topic(topic)
        res = get_response_from_dict(topic, "location")
        dispatcher.utter_message(text=res)
        return []


class ActionGetSpell(Action):
    """Get the spell upgrade for a topic from the knowledge base"""
    def name(self) -> Text:
        return "action_get_spell"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = get_topic(topic)
        res = get_response_from_dict(topic, "spell_upgrade")
        dispatcher.utter_message(text=res)
        return []

class ActionGetWeapon(Action):
    """Get the weapon damage for a topic from the knowledge base"""
    def name(self) -> Text:
        return "action_get_weapon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = get_topic(topic)
        res = get_response_from_dict(topic, "weapon_damage")
        dispatcher.utter_message(text=res)
        return []
