import json
filename =

def add_new_teacher(subject, name, description='', rating=-1, number=None):
    with open(filename, 'r') as f:
        teachers = json.load(f)
        teachers[subject][name] = {"feedback": [], "ratings": []}
        if description != '':
            teachers[subject][name]["feedback"].append(description)
        if int(rating) >= 0:
            teachers[subject][name]["ratings"].append(int(rating))
        teachers[subject][name]["number"] = number
    with open(filename, 'w') as f:
        json.dump(teachers, f)


def add_new_description(subject, name, description ='', rating = -1, number = None):
    with open(filename, 'r') as f:
        teachers = json.load(f)
        if description != '':
            teachers[subject][name]["feedback"].append(description)
        if int(rating) >= 0:
            teachers[subject][name]["ratings"].append(int(rating))
        teachers[subject][name]["number"] = number
    with open(filename, 'w') as f:
        json.dump(teachers, f)


def find_teachers(subject, st):
    with open(filename, 'r') as f:
        ret = []
        teachers = json.load(f)
        for i in teachers[subject].keys():
            #print(i)
            if st in i or st in str(teachers[subject][i]['number']):
                ret.append(i)
        return ret

def read_teacher(subject, name):
    with open(filename, 'r') as f:
        teachers = json.load(f)
        if name not in teachers[subject].keys():
            return None
        return teachers[subject][name]


