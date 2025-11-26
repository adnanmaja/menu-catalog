from google import genai
from google.genai import errors
import os
from dotenv import load_dotenv
from ..models.model import Menu

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

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
        
    def classify_alergen(self, menu):
        prompt = f""" 
        Any alergens in the item below?
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
    
    



