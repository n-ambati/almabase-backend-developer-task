import json
from json.decoder import JSONDecodeError
from fuzzywuzzy import fuzz
import multiprocessing
from multiprocessing import Process


def is_same(profile1: dict, profile2: dict, field: str) -> int:
    if field in profile1 and profile1[field] and field in profile2 and profile2[field]:
        if profile1[field] == profile2[field]:
            return 1
        return -1
    return 0


def compute_similarity_score(profile1: dict, profile2: dict, fields: list, result: list) -> tuple:
    total_match_score = 0   # Initialise total match score

    first_name_score = 0
    last_name_score = 0
    email_score = 0
    denominator = 0
    flag = False

    matching_attributes = []
    non_matching_attributes = []
    ignored_attributes = []

    if 'email' in fields:
        email_score = fuzz.ratio(profile1['email'], profile2['email'])
        denominator += 100
    else:
        ignored_attributes.append('email')

    if 'first_name' in fields:
        first_name_score = fuzz.ratio(profile1['first_name'], profile2['first_name'])
        denominator += 100
    else:
        ignored_attributes.append('first_name')

    if 'last_name' in fields:
        last_name_score = fuzz.ratio(profile1['last_name'], profile2['last_name'])
        denominator += 100
    else:
        ignored_attributes.append('last_name')

    if ((first_name_score + last_name_score + email_score) / denominator) > 0.8:
        total_match_score += 1
        flag = True


    for field in fields:
        if field in set(['first_name', 'last_name', 'email']) and field not in ignored_attributes:
            if flag:
                matching_attributes.append(field)
            else:
                non_matching_attributes.append(field)
            continue

        similarity = is_same(profile1, profile2, field)
        total_match_score += similarity

        if similarity == 1:
            matching_attributes.append(field)
        elif similarity == -1:
            non_matching_attributes.append(field)
        else:
            ignored_attributes.append(field)

    ignored_attributes += list(
        set(profile1.keys()).union(set(profile2.keys())).difference(set(matching_attributes + non_matching_attributes + ignored_attributes))
    )
    ignored_attributes.remove('id')

    result.append({
        'profiles': [f'profile{profile1["id"]}', f'profile{profile2["id"]}'],
        'total_match_score': total_match_score,
        'matching_attributes': matching_attributes if len(matching_attributes) > 0 else None,
        'non_matching_attributes': non_matching_attributes if len(non_matching_attributes) > 0 else None,
        'ignored_attributes': ignored_attributes if len(ignored_attributes) > 0 else None
    })


def save(result):
    with open('result.json', 'w') as f:
        data = {'result': list(result)}
        json.dump(data, f)


def find_result(profiles: list, fields: list):
    processes = []
    manager = multiprocessing.Manager()
    result = manager.list()
    for i in range(len(profiles) - 1):
        for j in range(i + 1, len(profiles)):
            p = Process(target=compute_similarity_score, args=(profiles[i], profiles[j], fields, result))
            p.start()
            processes.append(p)

    for process in processes:
        process.join()

    if len(result) > 0:
        save(result)


def main():
    profile1 = {
        'id': 1,
        'email': 'knowkanhai@gmail.com',
        'first_name': 'Kanhai',
        'last_name': 'Shah',
        'class_year': None,
        'date_of_birth': None
    }
    profile2 = {
        'id': 2,
        'email': 'knowkanhai+donotcompare@gmail.com',
        'first_name': 'Kanhai1',
        'last_name': 'Shah',
        'class_year': 2012,
        'date_of_birth': '1990-10-11'
    }

    profiles = [profile1, profile2]
    fields = ['first_name', 'last_name']

    find_result(profiles, fields)


if __name__ == '__main__':
    main()
