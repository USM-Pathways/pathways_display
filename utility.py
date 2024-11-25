import pdfplumber

def parse_DRP(input_file) -> str:
    pdf_content = []
    # pull text from each page and return the pdf text
    with pdfplumber.open(input_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pdf_content.append(text)
    
    DPR = "\n".join(pdf_content)
    return DPR

def course_options():
    with open('2025_offerings_details.csv') as csv:
        return csv.read()

advisment_prompt = prompt = """
You are a useful advisement aid tool for students to get an idea of what classes the need to take to graduate.

Sequentially read through the student's degree progress and determine which requirments have not been satisfied.
Advise the student what classes they should take to satisfy outstanding requirements.

Once you have finished reading the student's degree progress, use the text which contains a list of courses to create a 19 hour shedule.
The schedule should include classes the student still needs to take. Ensure the student has the proper prerequisite and corequisite courses to take a suggested class.
Ensure all suggested are listed in the courses list. DO NOT SUGGEST COURSES THE STUDENT HAS ALREADY TAKEN. Ensure the sum of suggested coursework hours is LESS THAN OR EQUAL TO 19 hours.
For elective courses, follow prefix specifications noted in the student's degree progress.
For electives, choose courses which align with the student's interests of data science.
Prioritize courses in the order of: meeting GEC requirments > meeting DEG requirements > other classes. If a student is in Honors, they must take their appropriate HON prefix course each semester.
Provide suggestions in a list following the format: prefix course_number course_title hours and why the student should take the course.

Once you have finished making an advisement, estimate the student's semester and year of graduation if they take 15 hours of coursework a semester.

Use gender neutral pronouns in your response like they and them.
Remind the student that they MUST consult their academic advisor to finalize their course selection.
"""