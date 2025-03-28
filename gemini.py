import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def setup_firebase(service_account_path, database_url):
    """Sets up Firebase connection."""
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url,
    })

def get_gemini_response(prompt):
    """Gets a response from Gemini 1.5 Flash."""
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        parts = response.candidates[0].content.parts
        text = ' '.join(part.text for part in parts)
        return text
    except Exception as e:
        return f"Error during Gemini analysis: {e}"

def analyze_student_data_with_gemini(student_id):
    """
    Retrieves student data from Firebase, analyzes it using Gemini 1.5 Flash,
    and returns the analysis.
    """
    students_ref = db.reference('Students')
    student_data = students_ref.child(student_id).get()

    if student_data:
        data_string = str(student_data)
        prompt = f"Analyze the following student data and provide a summary of key information, including academic performance, major, and any notable characteristics:\n\n{data_string}"
        return get_gemini_response(prompt)
    else:
        return f"Student with ID {student_id} not found in Firebase."

def main():
    """Main function to retrieve and analyze student data."""
    service_account_path = "serviceAccountKey.json"
    database_url = "https://imageattandance-default-rtdb.asia-southeast1.firebasedatabase.app/"

    setup_firebase(service_account_path, database_url)

    student_id_to_analyze = input("Enter the Student ID to analyze: ")

    analysis_result = analyze_student_data_with_gemini(student_id_to_analyze)
    print(f"\nAnalysis for Student ID: {student_id_to_analyze}")
    print(analysis_result)

if __name__ == "__main__":
    main()