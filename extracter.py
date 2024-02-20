<<<<<<< HEAD
import PyPDF2
import re
from openai import OpenAI, ChatCompletion
import pickle
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud


# Set your OpenAI API key here
# api_key = "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"

# Initialize OpenAI client with your API key
# client = OpenAI(api_key=api_key)

# def get_openai_response(prompt):
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an AI assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return completion.choices[0].message


def extract_text_from_pdf(file_path):
    pdf = PyPDF2.PdfReader(file_path)
    text = pdf.pages[0].extract_text()
    return text

def extract_email(text):
    # Regular expression to match an email address
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Search for the email pattern in the text
    match = re.search(email_regex, text)
    
    if match:
        return match.group()
    else:
        return None

def extract_skills(text):
    skill_patterns = [
    r'Python', r'Java', r'C\+\+', r'HTML', r'CSS', r'JavaScript', r'Flask', r'DoctPlus', 
    r'NextJS', r'TypeScript', r'Tailwind CSS', r'Firebase', r'Next auth', 
    r'JavaScript', r'Clerk auth', r'react email', r'Resend', r'Bootstrap', 
    r'Node\.js', r'ExpressJS', r'NextJS', r'TAILWIND CSS', 
    r'NODEJS', r'EXPRESSJS', r'Machine Learning', r'Deep Learning', r'Artificial Intelligence', 
    r'Data Science', r'Big Data', r'Cloud Computing', r'Cybersecurity', r'Database Management', 
    r'Network Administration', r'UI/UX Design', r'Mobile Development', r'Web Design', r'Project Management', 
    r'Agile Methodology', r'Problem-solving', r'Creativity', r'Critical Thinking', r'Communication Skills', 
    r'Teamwork', r'Leadership', r'Time Management', r'Adaptability', r'Attention to Detail', r'Analytical Skills',
    r'OpenCV', r'Mediapipe', r'Django', r'Angular', r'React', r'Vue.js', r'SQL', r'MongoDB', r'Swift', 
    r'Android', r'iOS', r'Ruby', r'PHP', r'Node.js', r'Express.js', r'UI Design', r'UX Design', r'Mobile App Development',
    r'Web Development', r'Frontend Development', r'Backend Development', r'Database Administration', 
    r'Network Security', r'Cybersecurity', r'Cloud Architecture', r'Cloud Services', r'Agile Development', 
    r'Software Engineering', r'DevOps', r'Project Planning', r'Project Coordination', r'Problem-solving', 
    r'Collaboration', r'Interpersonal Skills', r'Presentation Skills', r'Data Analysis', r'Data Visualization', 
    r'Mathematics', r'Statistics', r'Algorithms', r'Problem-solving', r'Critical Thinking', r'Troubleshooting',
    r'UX/UI Design', r'Figma', r'Adobe XD', r'Sketch', r'InVision', r'Zeplin', r'Principle', r'Canva', 
    r'Photoshop', r'Illustrator', r'PowerPoint', r'Keynote', r'Google Slides', r'Git', r'Github'
]

    
    # Compile regular expressions
    skill_regex = re.compile('|'.join(skill_patterns), re.IGNORECASE)
    
    # Find all matches in the text
    matches = skill_regex.findall(text)
    
    # Convert matches to lowercase and remove duplicates
    skills = list(set(map(str.lower, matches)))
    
    # Return unique skills
    return skills

def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)  
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

def resumeDet(text):
    # Load the trained classifier
    clf = pickle.load(open('clf.pkl', 'rb'))
    tfidf = pickle.load(open('tfidf.pkl', 'rb'))

    # Clean the input resume
    cleaned_resume = cleanResume(text)

    # Transform the cleaned resume using the trained TfidfVectorizer
    input_features = tfidf.transform([cleaned_resume])

    # Make the prediction using the loaded classifier
    prediction_id = clf.predict(input_features)[0]

    # Map category ID to category name
    category_mapping = {
        15: "Java Developer",
        23: "Testing",
        8: "DevOps Engineer",
        20: "Python Developer",
        24: "Web Designing",
        12: "HR",
        13: "Hadoop",
        3: "Blockchain",
        10: "ETL Developer",
        18: "Operations Manager",
        6: "Data Science",
        22: "Sales",
        16: "Mechanical Engineer",
        1: "Arts",
        7: "Database",
        11: "Electrical Engineering",
        14: "Health and fitness",
        19: "PMO",
        4: "Business Analyst",
        9: "DotNet Developer",
        2: "Automation Testing",
        17: "Network Security Engineer",
        21: "SAP Developer",
        5: "Civil Engineer",
        0: "Advocate",
    }

    category_name = category_mapping.get(prediction_id, "Unknown")

    print("Predicted Category:", category_name)
    return category_name


def experience(text):
    # Initialize variables to store job, education, and experience
    job = ""
    education = ""
    experience = ""

    # Find occurrences of 'Skill Details' to determine the structure of the text
    if 'Skill Details' in text:
        # Split the text into sections based on 'Skill Details'
        sections = text.split("Skill Details", 1)

        if len(sections) == 2:
            experience = sections[1].strip()  # Extract experience

            # Split the section before 'Skill Details' into lines
            lines = sections[0].strip().split('\n')

            # Extract job and education details from the lines
            if len(lines) >= 4:
                job = "\n".join(lines[-4:])  # Last 4 lines for job
                education = "\n".join(lines[:-4])  # All lines before job for education

    return job, education, experience


# def extract_achievements(text):
#     user_input = text + ' What are the achievements? '
#     response = get_openai_response(user_input)
#     print("AI: ", response)   

#     pattern = r'\d+\s+(.+?)\s*(?=n\d|$)'

#     # Extract individual achievements using regular expression
#     achievements = re.findall(pattern, text)
#     return achievements


# file_path = 'resume.pdf'
# resume_text = extract_text_from_pdf(file_path)
# email = extract_email(resume_text)
# if email:
#     print("Extracted email:", email)
# else:
#     print("No email found in the resume.")
=======
import PyPDF2
import re
from openai import OpenAI, ChatCompletion
import pickle
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud


# Set your OpenAI API key here
# api_key = "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"

# Initialize OpenAI client with your API key
# client = OpenAI(api_key=api_key)

# def get_openai_response(prompt):
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an AI assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return completion.choices[0].message


def extract_text_from_pdf(file_path):
    pdf = PyPDF2.PdfReader(file_path)
    text = pdf.pages[0].extract_text()
    return text

def extract_email(text):
    # Regular expression to match an email address
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Search for the email pattern in the text
    match = re.search(email_regex, text)
    
    if match:
        return match.group()
    else:
        return None

def extract_skills(text):
    skill_patterns = [
    r'Python', r'Java', r'C\+\+', r'HTML', r'CSS', r'JavaScript', r'Flask', r'DoctPlus', 
    r'NextJS', r'TypeScript', r'Tailwind CSS', r'Firebase', r'Next auth', 
    r'JavaScript', r'Clerk auth', r'react email', r'Resend', r'Bootstrap', 
    r'Node\.js', r'ExpressJS', r'NextJS', r'TAILWIND CSS', 
    r'NODEJS', r'EXPRESSJS', r'Machine Learning', r'Deep Learning', r'Artificial Intelligence', 
    r'Data Science', r'Big Data', r'Cloud Computing', r'Cybersecurity', r'Database Management', 
    r'Network Administration', r'UI/UX Design', r'Mobile Development', r'Web Design', r'Project Management', 
    r'Agile Methodology', r'Problem-solving', r'Creativity', r'Critical Thinking', r'Communication Skills', 
    r'Teamwork', r'Leadership', r'Time Management', r'Adaptability', r'Attention to Detail', r'Analytical Skills',
    r'OpenCV', r'Mediapipe', r'Django', r'Angular', r'React', r'Vue.js', r'SQL', r'MongoDB', r'Swift', 
    r'Android', r'iOS', r'Ruby', r'PHP', r'Node.js', r'Express.js', r'UI Design', r'UX Design', r'Mobile App Development',
    r'Web Development', r'Frontend Development', r'Backend Development', r'Database Administration', 
    r'Network Security', r'Cybersecurity', r'Cloud Architecture', r'Cloud Services', r'Agile Development', 
    r'Software Engineering', r'DevOps', r'Project Planning', r'Project Coordination', r'Problem-solving', 
    r'Collaboration', r'Interpersonal Skills', r'Presentation Skills', r'Data Analysis', r'Data Visualization', 
    r'Mathematics', r'Statistics', r'Algorithms', r'Problem-solving', r'Critical Thinking', r'Troubleshooting',
    r'UX/UI Design', r'Figma', r'Adobe XD', r'Sketch', r'InVision', r'Zeplin', r'Principle', r'Canva', 
    r'Photoshop', r'Illustrator', r'PowerPoint', r'Keynote', r'Google Slides', r'Git', r'Github'
]

    
    # Compile regular expressions
    skill_regex = re.compile('|'.join(skill_patterns), re.IGNORECASE)
    
    # Find all matches in the text
    matches = skill_regex.findall(text)
    
    # Convert matches to lowercase and remove duplicates
    skills = list(set(map(str.lower, matches)))
    
    # Return unique skills
    return skills

def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)  
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

def resumeDet(text):
    # Load the trained classifier
    clf = pickle.load(open('clf.pkl', 'rb'))
    tfidf = pickle.load(open('tfidf.pkl', 'rb'))

    # Clean the input resume
    cleaned_resume = cleanResume(text)

    # Transform the cleaned resume using the trained TfidfVectorizer
    input_features = tfidf.transform([cleaned_resume])

    # Make the prediction using the loaded classifier
    prediction_id = clf.predict(input_features)[0]

    # Map category ID to category name
    category_mapping = {
        15: "Java Developer",
        23: "Testing",
        8: "DevOps Engineer",
        20: "Python Developer",
        24: "Web Designing",
        12: "HR",
        13: "Hadoop",
        3: "Blockchain",
        10: "ETL Developer",
        18: "Operations Manager",
        6: "Data Science",
        22: "Sales",
        16: "Mechanical Engineer",
        1: "Arts",
        7: "Database",
        11: "Electrical Engineering",
        14: "Health and fitness",
        19: "PMO",
        4: "Business Analyst",
        9: "DotNet Developer",
        2: "Automation Testing",
        17: "Network Security Engineer",
        21: "SAP Developer",
        5: "Civil Engineer",
        0: "Advocate",
    }

    category_name = category_mapping.get(prediction_id, "Unknown")

    print("Predicted Category:", category_name)
    return category_name


def experience(text):
    # Initialize variables to store job, education, and experience
    job = ""
    education = ""
    experience = ""

    # Find occurrences of 'Skill Details' to determine the structure of the text
    if 'Skill Details' in text:
        # Split the text into sections based on 'Skill Details'
        sections = text.split("Skill Details", 1)

        if len(sections) == 2:
            experience = sections[1].strip()  # Extract experience

            # Split the section before 'Skill Details' into lines
            lines = sections[0].strip().split('\n')

            # Extract job and education details from the lines
            if len(lines) >= 4:
                job = "\n".join(lines[-4:])  # Last 4 lines for job
                education = "\n".join(lines[:-4])  # All lines before job for education

    return job, education, experience


# def extract_achievements(text):
#     user_input = text + ' What are the achievements? '
#     response = get_openai_response(user_input)
#     print("AI: ", response)   

#     pattern = r'\d+\s+(.+?)\s*(?=n\d|$)'

#     # Extract individual achievements using regular expression
#     achievements = re.findall(pattern, text)
#     return achievements


# file_path = 'resume.pdf'
# resume_text = extract_text_from_pdf(file_path)
# email = extract_email(resume_text)
# if email:
#     print("Extracted email:", email)
# else:
#     print("No email found in the resume.")
>>>>>>> acc25e2b08ad1280501d3ae1b3b1a250dc4cdc83
