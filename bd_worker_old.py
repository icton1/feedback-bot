import json


def add_new_teacher(name, description='', rating=-1, number=None):
    with open('teachers.json', 'r') as f:
        teachers = json.load(f)
        teachers[name] = {"feedback": [], "ratings": []}
        if description != '':
            teachers[name]["feedback"].append(description)
        if int(rating) >= 0:
            teachers[name]["ratings"].append(int(rating))
        teachers[name]["number"] = number
    with open('teachers.json', 'w') as f:
        json.dump(teachers, f)


def add_new_description(name, description ='', rating = -1, number = None):
    with open('teachers.json', 'r') as f:
        teachers = json.load(f)
        if description != '':
            teachers[name]["feedback"].append(description)
        if int(rating) >= 0:
            teachers[name]["ratings"].append(int(rating))
        teachers[name]["number"] = number
    with open('teachers.json', 'w') as f:
        json.dump(teachers, f)


def find_teachers(st):
    with open('teachers.json', 'r') as f:
        ret = []
        teachers = json.load(f)
        for i in teachers.keys():
            #print(i)
            if st in i or st in str(teachers[i]['number']):
                ret.append(i)
        return ret

def read_teacher(name):
    with open('teachers.json', 'r') as f:
        teachers = json.load(f)
        if name not in teachers.keys():
            return None
        return teachers[name]


