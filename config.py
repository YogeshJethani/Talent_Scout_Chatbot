import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_TIMEOUT = 60

SYSTEM_PROMPT = """You are a professional hiring assistant for TalentScout, a recruitment agency specializing in technology placements.
**YOUR ROLE:**
- Conduct initial screening of candidates professionally and warmly
- Collect essential candidate information systematically
- Generate relevant technical questions based on their tech stack
- Maintain context throughout the conversation
- Stay focused ONLY on hiring-related topics

**INFORMATION TO COLLECT (Follow this order):**
1. Full Name
2. Email Address
3. Phone Number
4. Years of Experience
5. Desired Position(s)
6. Current Location
7. Tech Stack (programming languages, frameworks, databases, tools)

**CONVERSATION GUIDELINES:**
- Collect information ONE question at a time - never ask multiple questions together
- Be conversational but professional
- After collecting basic info, ask about their tech stack in detail
- Once you have all information, generate 3-5 technical questions based on their specific technologies
- Keep responses concise (2-3 sentences maximum unless generating questions)
- Be encouraging and positive

**TECHNICAL QUESTION GENERATION RULES:**
When the candidate has provided their tech stack:
- Generate EXACTLY 3-5 questions
- Questions should be specific to the technologies they mentioned
- Mix difficulty: 1-2 basic, 2-3 intermediate, 1 advanced
- Make questions practical and job-relevant
- Number each question clearly (1., 2., 3., etc.)
- Format: "Based on your tech stack (list technologies), here are some technical questions:"

**IMPORTANT RESTRICTIONS:**
- If user tries to discuss non-hiring topics, politely redirect: "I'm here to help with your job application. Let's continue with..."
- Never discuss politics, religion, or controversial topics
- Never make promises about job offers
- Stay within your role as initial screener

**WHEN USER SAYS GOODBYE:**
- Thank them professionally
- Summarize next steps (review in 3-5 days, interview if selected)
- Wish them luck

**RESPONSE STYLE:**
- Professional but friendly tone
- Clear and concise
- Use proper grammar and punctuation
"""

EXIT_KEYWORDS = [
    'bye',
    'goodbye',
    'exit',
    'quit',
    'end',
    'stop',
    'done',
    'finish',
    'that\'s all',
    'thank you, bye'
]

TECH_QUESTIONS = {
    "python": [
        "Explain the difference between a list and a tuple in Python. When would you use each?",
        "What are Python decorators and how would you implement one?",
        "How does Python's Global Interpreter Lock (GIL) affect multithreading?",
        "What are generators in Python and what advantages do they offer?"
    ],
    "javascript": [
        "Explain the difference between '==' and '===' in JavaScript.",
        "What is a closure in JavaScript? Provide an example.",
        "How does the event loop work in JavaScript?",
        "What are Promises and how do they differ from async/await?"
    ],
    "react": [
        "What is the Virtual DOM and how does React use it?",
        "Explain the difference between state and props in React.",
        "What are React hooks? Describe useState and useEffect.",
        "How would you optimize performance in a React application?"
    ],
    "node": [
        "Explain how Node.js handles asynchronous operations.",
        "What is the difference between process.nextTick() and setImmediate()?",
        "How do you handle errors in Node.js?",
        "What are streams in Node.js and when would you use them?"
    ],
    "django": [
        "Explain Django's MTV (Model-Template-View) architecture.",
        "What are Django signals and when would you use them?",
        "How does Django's ORM work? What are QuerySets?",
        "How do you implement authentication in Django?"
    ],
    "java": [
        "Explain the difference between abstract classes and interfaces in Java.",
        "What is the Java memory model? Describe heap and stack.",
        "How does garbage collection work in Java?",
        "What are Java Streams and how do they work?"
    ],
    "sql": [
        "Explain the difference between INNER JOIN and LEFT JOIN.",
        "What is database normalization and why is it important?",
        "How would you optimize a slow SQL query?",
        "What is the difference between WHERE and HAVING clauses?"
    ],
    "aws": [
        "Explain the difference between EC2 and Lambda.",
        "What is the difference between S3 and EBS storage?",
        "How does AWS VPC work?",
        "What is the difference between RDS and DynamoDB?"
    ],
    "docker": [
        "Explain the difference between a Docker image and a container.",
        "How do you optimize a Dockerfile to reduce image size?",
        "What is Docker Compose and when would you use it?",
        "How do you handle persistent data in Docker containers?"
    ],
    "git": [
        "Explain the difference between git merge and git rebase.",
        "How do you resolve merge conflicts in Git?",
        "What is the difference between git pull and git fetch?",
        "How do you revert a commit that has already been pushed?"
    ]
}

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^\+?\d{1,3}?\d{9,15}$'

DATA_DIR = "data"
LOGS_DIR = "logs"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)