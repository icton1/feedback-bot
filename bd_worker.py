import json


def add_new_teacher(name, description, rating, number=None):
    with open('teachers.json', 'r') as f:
        teachers = json.load(f)
        teachers[name] = {"feedback": [], "ratings": []}
        teachers[name]["feedback"].append(description)
        teachers[name]["ratings"].append(rating)
        teachers[name]["number"]=number
    with open('teachers.json', 'w') as f:
        json.dump(teachers, f)


def add_new_description(name, description, rating, number = None):
    with open('teachers.json', 'r') as f:
        teachers = json.load(f)
        teachers[name]["feedback"].append(description)
        teachers[name]["ratings"].append(rating)
        teachers[name]["number"] = number
    with open('teachers.json', 'w') as f:
        json.dump(teachers, f)


def find_teacher(st):
    with open('teachers.json', 'r') as f:
        ret = []
        teachers = json.load(f)
        for i in teachers.keys():
            if st in i or st in teachers[i]['number']:
                ret.append(i)
        return ret

def read_teacher(name):
    with open('teachers.json', 'r') as f:
        teachers = json.load(f)
        return teachers[name]

add_new_teacher('k3k', 'молодец', 10, 1337)
add_new_description('k3k', 'ууу((', -10, 1337)
print(read_teacher(find_teacher('k')[0]))