import utilities
import duplicate_finder


def main():
    data = utilities.read_input()

    if data is None:
        print('Invalid Input!')
        return

    profiles = data['profiles']
    fields = data['fields']
    result = duplicate_finder.find_duplicates(profiles, fields)

    if len(result) > 0:
        utilities.save(result)


if __name__ == '__main__':
    main()
