
import sys
import datetime
from clippings.models import Clip

def parse_title_author(s):
    s = s.split('(')
    title = s[0].strip()

    #special case when there is a parenthesis in the title
    if (len(s) > 2):
        author = s[2].strip(')\n')
    else:
        author = s[1].strip(')\n')  

    #special case when author name is reversed and seperated by comma
    if ',' in author:
        split = author.split(',')
        author = split[1].strip() + " " + split[0]

    return title, author

def parse_date(month, day, year, time, aorpm):
    date_str = month + " " + day + " " + year + " " + time + " " + aorpm
    return datetime.datetime.strptime(date_str, '%B %d, %Y %I:%M:%S %p')

def parse_metadata(s):
    s = s.split()
    #special case where page number is missing, add a default page of 0
    if (len(s) == 15):
        s.insert(4, "page")
        s.insert(5, 0)
        s.insert(6, "|")
    page = int(s[5])
    location = s[8] #keep as string
    date = parse_date(s[13], s[14], s[15], s[16], s[17]) 
    return page, location, date


def parse_file(full_path, db, current_user):
    with open(full_path, 'r') as f:
        lines = list(f)
        i = 0
        count = 0
        for line in lines:
            if (i%5 == 0):
                title, author = parse_title_author(line)
                page, location, date = parse_metadata(lines[i+1])
                clipping = lines[i+3].strip()
                
                clip = Clip(title=title,
                            author=author,
                            page=page,
                            location=location,
                            date=date,
                            clipping=clipping,
                            user_id=current_user.id)
                db.session.add(clip)
                count +=1
            i +=1
        db.session.commit()
        return count
