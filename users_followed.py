import os
import errno
import logging
import time
import argparse
import configparser
from github import Github
from tqdm import tqdm

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    users = args.user.split(',')

    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['github']['username']
    password = config['github']['password']

    g = Github(username, password)

    try:
        os.makedirs('Exports/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    for username in users:
        username = g.get_user(username)
        following = username.get_following()
        for u in tqdm(enumerate(following, 1), total=following.totalCount, dynamic_ncols=True):
            with open(f"Exports/{username.login}_following.csv") as f:
                for user in following:
                    f.write(f"{user.login}\n")

    logger.info("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Python skeleton')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-u', '--user', help="Users to search (separated by comma)", type=str)
    parser.set_defaults(boolean_flag=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()

