from flask import Flask, jsonify
import extracter

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def display_text():
    text = extracter.extract_text_from_pdf('resume.pdf')
    email = extracter.extract_email(text)
    skills = extracter.extract_skills(text)
    # ach = str(extracter.extract_point(text))
    # ach = extracter.cleanResume(ach)
    exp = extracter.experience(text)
    catagory = extracter.resumeDet(text)
    if email:
        result = {
            "Email": email,
            "Text" : text,
            "Skills" : skills, 
            # "Ach" : ach,
            "Catagory" : catagory,
            "Experience" : exp,
        }    
    else:
        result = {
            "Email": "Unknown",
            "Text" : "Unknown",
            "Skills" : "Not found",
            # "Ach" : ach,
            "Catagory" : "Unknown",
            "Experience" : "Unknown",
        }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port="3000")

