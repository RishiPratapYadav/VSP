import os
import google.generativeai as genai

# --- Configuration ---
# This script reads the same environment variable as your main app.
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set it in your terminal before running the script, for example:")
    print("export GOOGLE_API_KEY='YOUR_API_KEY_HERE'")
else:
    try:
        genai.configure(api_key=api_key)

        print("✅ Finding models available to your API key that support 'generateContent'...\n")

        found_models = False
        for model in genai.list_models():
            # The 'generateContent' method is used for general-purpose prompting
            # which is what this application needs.
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name} ")
                print(f"- {model.quote} ")
                found_models = True

        if not found_models:
            print("No suitable models found. There might be an issue with your API key or project setup.")
        else:
            print("\nThese are the models you can use in your main.py file.")
            print("Using one of the 'latest' models, like 'gemini-1.5-pro-latest', is usually a great choice.")

    except Exception as e:
        print(f"An error occurred while trying to list models: {e}")
        print("Please ensure your API key is correct and has the 'Generative Language API' enabled in your Google Cloud project.")

