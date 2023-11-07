import hashlib

if __name__ == '__main__':
    # must match with the rest of the SQL schema
    ROLE_NAME = 'maintainer'
    print("type postgres password for to hash")
    pwd = input().strip('\n')
    print("md5" + hashlib.md5(bytes(pwd, 'utf-8') + bytes(ROLE_NAME, 'utf-8')).hexdigest())