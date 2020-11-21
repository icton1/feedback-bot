import json
filename = 'subjects.json'


def add_new_teacher(subject, name, description='', rating=-1, number=None):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        subjects_fo[subject][name] = {"feedback": [], "ratings": []}
        if description != '':
            subjects_fo[subject][name]["feedback"].append(description)
        if int(rating) >= 0:
            subjects_fo[subject][name]["ratings"].append(int(rating))
        subjects_fo[subject][name]["number"] = number
    with open(filename, 'w') as f:
        json.dump(subjects_fo, f)


def add_new_description(subject, name, description ='', rating = -1, number = None):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        if description != '':
            subjects_fo[subject][name]["feedback"].append(description)
        if int(rating) >= 0:
            subjects_fo[subject][name]["ratings"].append(int(rating))
        subjects_fo[subject][name]["number"] = number
    with open(filename, 'w') as f:
        json.dump(subjects_fo, f)


def find_teachers(subject, st):
    with open(filename, 'r') as f:
        ret = []
        subjects_fo = json.load(f)
        for i in subjects_fo[subject].keys():
            #print(i)
            if st in i or st in str(subjects_fo[subject][i]['number']):
                ret.append(i)
        return ret

def read_teacher(subject, name):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        if name not in subjects_fo[subject].keys():
            return None
        return subjects_fo[subject][name]


"""---------------------------------------"""
def add_new_subject(name):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        subjects_fo[name] = {}
    with open(filename, 'w') as f:
        json.dump(subjects_fo, f)

def find_subject(st):
    with open(filename, 'r') as f:
        ret = []
        subjects_fo = json.load(f)
        for i in subjects_fo.keys():
            if st in i:
                ret.append(i)
        return ret

def read_subject(name):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        if name not in subjects_fo.keys():
            return None
        return subjects_fo[name]

