from google import genai
from google.genai import errors
import os
from dotenv import load_dotenv
from ..models.model import Menu

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY_2')

class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)

    def generate_menu_description(self, menu):
        prompt = f"""
        Write a very short menu description of this item:
        Name: {menu.name}
        Category: {menu.category}
        Ingredients: {menu.ingredients}
        Current Description: {menu.description}
        Keep it very short, max 10 words ig. Also keep it pure string, and dont use escape sequences
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text
    
    def generate_category(self, menu):
        prompt = f""" 
        Categorize this item. Available categories are: drinks, appetizers, desserts, main course
        Name: {menu.name}
        Current category: {menu.category}
        Ingredients: {menu.ingredients}
        Description: {menu.description}
        use one of the available categories listed above (this is important) ok? dont make stuff up
        """
    
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text.strip().lower()
        
    def classify_allergen(self, menu):
        prompt = f""" 
        Any allergens in the item below?
        Name: {menu.name}
        Category: {menu.category}
        Ingredients: {menu.ingredients}
        if yes, list them out like this: nuts, dairy, eggs. if there's none, just say: none
        dont use newlines or bullets pls.
        """
    
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text.strip().lower()
    
    def translate_description(self, menu, language):
        prompt = f""" 
        Can you translate this description into {language} language?
        Description: {menu.description}
        just give me the translation, no need to explain anything, keep it concise.
        """
    
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text
    
    def natural_language_query(self, query):
        print("nl query called")
        prompt = f"""
        You are an AI that converts natural language search queries 
        into SQL-style filter instructions for a menu database.

        The menu schema:
        - name (string)
        - category (string)
        - calories (float)
        - price (float)
        - description (string)
        - ingredients (string[]) # its an array of strings

        Given the user's query: "{query}"

        Extract these fields:

        
        "name_contains": "[]",
        "category": "string",
        "min_price": "float",
        "max_price": "float",
        "min_calories": "float",
        "max_calories": "float"
        
        available categories are: drinks, appetizers, desserts, main course
        for name_contains, can you do it in bahasa? so, the query might say 'coffee', but put 'kopi' in it
        for prices and calories, just accept any number

        Only extract filters explicitly mentioned (except category, probably). No guessing.
        Respond in valid JSON only.
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text
    



