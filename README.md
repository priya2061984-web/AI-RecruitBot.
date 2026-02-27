AI Hiring Assistant Chatbot –


Project Explanation Project Overview (What is this chatbot?) The AI Hiring Assistant Chatbot is an intelligent recruitment automation system built using Streamlit and Google Gemini API. It acts as a virtual technical interviewer that collects candidate details, generates skill-based technical questions, analyzes candidate responses using AI, and stores interview data in structured formats such as CSV and JSON.

What Problem It Solves : Traditional recruitment screening is time-consuming, repetitive, and difficult to scale for large applicant pools. This chatbot automates the initial technical screening process, generates customized questions, reduces manual HR effort, and provides structured candidate information for faster decision-making.

How It Collects User Data:The chatbot collects candidate information through Streamlit input components such as text inputs, number inputs, and text areas. The collected data is temporarily stored in Streamlit session state to maintain conversation context across multiple steps. 

How It Generates Technical Questions : The system uses the Gemini large language model to generate technical interview questions. A carefully designed prompt assigns the role of a professional technical interviewer and enforces constraints such as generating exactly five skill-based technical questions without including HR or behavioral questions.

Where Data Is Stored (JSON/CSV): After interview submission, candidate data is stored locally in two formats. A CSV file stores each candidate as a row for easy viewing in spreadsheet tools, while a JSON file stores structured candidate objects suitable for backend integration and analytics. 

Which Model/API Is Used : The project uses the Google Gemini API, specifically flash models, for both technical question generation and sentiment analysis. The API is integrated using the google-generativeai Python library.

How the Code Is Structured (Briefly) : The application follows a step-based architecture controlled using Streamlit session state. The workflow includes a greeting screen, candidate information collection, AI-based question generation, answer collection, sentiment analysis, data storage, and a completion screen. This structure ensures smooth interaction and controlled API usage.
