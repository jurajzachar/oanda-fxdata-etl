import hashlib
import secrets
import string
import argparse
from sys import exit

alphabet = string.ascii_letters + string.digits


def hash_pwd(pwd, role):
    return "md5" + hashlib.md5(bytes(pwd, 'utf-8') + bytes(role, 'utf-8')).hexdigest()


def gen_pwd(length=20):
    return ''.join(secrets.choice(alphabet) for i in range(length))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hash', action='store_true')
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--role', required=True)
    args = parser.parse_args()

    if args.hash and args.generate:
        print("Only one of --hash or --generate can be provided")
        exit(1)
    if not args.hash and not args.generate:
        print("Provide either --hash or --generate")
        exit(1)

    if args.hash:
        print("type postgres password to hash for role {args.role}")
        pwd = input().strip('\n')
        print(f"hashed password:\n{hash_pwd(pwd, args.role)}")
        exit(0)
    elif args.generate:
        pwd = gen_pwd()
        print(f"generated password:\n{pwd}")
        print(f"hashed password ({args.role}):\n{hash_pwd(pwd, args.role)}")
        exit(0)
