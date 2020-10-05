import requests
import hashlib
import sys


def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check api and try again.')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwnd_api(password):
    # check password if it exists in api response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwnd_api(password)
        if count:
            print(f'{password} was found {count} times..Change your password!')
        else:
            print(f'Password not found!')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
