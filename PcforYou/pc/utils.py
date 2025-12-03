from google import genai
from google.genai.errors import APIError
from django.conf import settings

def call_gemini_api(prompt):
    """
    Calls the Gemini API, ensuring a string is always returned.
    """
    try:
        # Check if the API key is set
        if not settings.GEMINI_API_KEY:
            return "ERROR: GEMINI_API_KEY not set in Django settings."

        # Initialize the Gemini Client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # Call the Model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=2048, 
                temperature=0.7 
            )
        )
        
        # Check for empty response content (which shouldn't happen normally)
        if not response.text:
             return "ERROR: Gemini returned an empty response."
             
        return response.text
        
    except APIError as e:
        # Handle specific API errors (e.g., key invalid, rate limit)
        # Always return a string here
        return f"ERROR: Gemini API Error occurred. Check key and billing: {e}"
        
    except Exception as e:
        # Handle general errors (e.g., network issues)
        # Always return a string here
        return f"ERROR: An unexpected Python error occurred: {e}"

    # : The implicit return None is now covered by the final 'except Exception'
    # but having comprehensive try/except blocks is the safest approach.