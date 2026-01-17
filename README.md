# Talent_Scout_Chatbot
TalentScout Hiring Assistant is an interactive chatbot designed to streamline the initial recruitment process for technology positions. It collects candidate information, understands their technical expertise, and generates relevant technical questions tailored to their declared tech stack.

# 🚀 Features

## Intelligent Information Gathering
Systematic collection of candidate details
Input validation for emails and phone numbers
Experience verification

## Dynamic Technical Assessment
Tech stack analysis
Customized question generation
Support for multiple technologies

## Conversation Management
Context-aware responses
Natural conversation flow
Exit detection and graceful endings

## User Interface
Clean, intuitive Streamlit interface
Real-time chat updates
Progress tracking sidebar
Conversation history display

# Data Management
Secure data storage
JSON-based candidate records
Timestamp-based file naming


# Example Conversation
Bot: Hello! Welcome to TalentScout's Hiring Assistant...
     What's your full name?

You: John Doe

Bot: Great! What's your email address?

You: john.doe@email.com

Bot: Thanks! What's your phone number?

You: +1-234-567-8900

Bot: How many years of professional experience do you have?

You: 5 years

Bot: What position(s) are you interested in?

You: Full Stack Developer

Bot: What's your current location?

You: San Francisco, CA

Bot: Please list your tech stack...

You: Python, Django, React, PostgreSQL, AWS

Bot: Based on your tech stack, here are technical questions:
     1. Explain Django's MTV architecture...
     2. What is the Virtual DOM in React...
     [etc.]
