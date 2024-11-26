import re, requests, json
from bs4 import BeautifulSoup

# get coid, course name, and general number from course description catalog
def parse_courses(url: str):
    page_count = get_page_count(url)
    
    course_links = dict()
    for page in range(1, page_count + 1):
        # append page filter to extract all course data
        filter = f'&filter%5Bcpage%5D={page}'
        
        response = requests.get(url + filter)
        soup = BeautifulSoup(response.content, "html.parser")
            
        content = soup.select('a[aria-expanded^="false"]')
        
        # extract and store course prefix, course number, and coid
        for line in content:
            link = line.get('href')
            coid = re.search(r'coid=(\d+)', str(link))
            parse = re.match(r"([A-Z]+) (\d+[A-Z]?)\s*-\s*(.+)", line.text)
            
            if parse and coid:
                if parse.group(1) not in course_links.keys():
                    course_links[parse.group(1)] = dict()
                
                course_links[parse.group(1)][parse.group(2)] = {
                    "name" : parse.group(3), 
                    "coid" : coid.group(1)
                }
    
    # store all parsed data
    file = open('course_paths.json', 'w')
    json.dump(course_links, file, indent = 4)
    file.close()

# get page count for usm course description catalog
def get_page_count(url: str):
    # get and parse url info
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    pages = soup.select('a[aria-label^="Page"]')
    
    # iterate through page data and extract highest page number
    page_count = 0
    for page in pages:
        try:
            current = int(page.text)
            page_count = current if current > page_count else page_count
        except ValueError:
            pass
    
    return page_count

def get_course_specifics():
    parsed_data = []

    with open('spring_2025_offerings.txt', 'r') as offerings:
        course_paths = open('course_paths.json')
        paths = json.load(course_paths)
        course_paths.close()

        for offering in offerings:
            course = re.match(r"([A-Z]+) (\d+[A-Z]?)", offering.strip())

            if course:
                try:
                    coid = paths[course.group(1)][course.group(2)]['coid']
                    url = f"https://catalog.usm.edu/preview_course_nopop.php?catoid=35&coid={coid}"

                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    targets = soup.find_all("p")

                    for target in targets:
                        if offering.strip() in target.text:
                            data = extract_info(target.text.strip())
                            
                            print(data) # logging
                            parsed_data.append(data)

                except KeyError:
                    pass

    with open('2025_offerings_details.txt', 'w') as out:
        output = "\n".join(parsed_data)
        out.write(output)

def extract_info(info: str):
    info = info.replace(u'\xa0', ' ')

    course_info = re.search(r"([A-Z]+) (\d+[A-Z]?) - (.+?)\s*(\d+(?:-\d+)?\s*hr\.?s?)", info)
    course_prefix = course_info.group(1) if course_info else "N/A"
    course_number = course_info.group(2) if course_info else "N/A"
    course_title = course_info.group(3) if course_info else "N/A"
    course_hours = course_info.group(4) if course_info else "hours not specified"


    if course_info:
        start, end = course_info.span()
        info = info[:start] + info[end:].strip()
    
    course_hours = course_hours.lstrip('.').strip()
    info = info.lstrip('. ').strip()

    return f'({course_hours}) {course_prefix} {course_number} - {course_title}: {info}'