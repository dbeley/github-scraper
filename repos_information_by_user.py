"""
Python script skeleton
"""
import os
import errno
import logging
import time
import argparse
import configparser
import pandas as pd
from github import Github
from tqdm import tqdm

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    users = args.user
    file = args.file
    if users:
        users = users.split(',')
    if file:
        with open(file, 'r') as f:
            users = f.readlines()
        users = [x.strip() for x in users]

    logger.debug(f"Users : {users}")
    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['github']['username']
    password = config['github']['password']

    g = Github(username, password)

    dict_complete = {}
    index_complete = 1
    for user in users:
        logger.info(f"Extracting repos information of {user}")

        dict_repos = {}
        user = g.get_user(user)
        repos = user.get_repos()
        for index, repo in tqdm(enumerate(repos, 1), total=user.public_repos, dynamic_ncols=True):
            dict = {}
            dict['User'] = user.login
            logger.debug(f"User : {dict['User']}")
            dict['Owner'] = repo.owner.login
            logger.debug(f"Owner : {dict['Owner']}")
            dict['Name'] = repo.name
            logger.debug(f"Name : {dict['Name']}")
            dict['URL'] = repo.html_url
            logger.debug(f"URL : {dict['URL']}")
            dict['Description'] = repo.description
            logger.debug(f"Description : {dict['Description']}")
            dict['Stars'] = repo.stargazers_count
            logger.debug(f"Stars : {dict['Stars']}")
            dict['Watchers'] = repo.watchers_count
            logger.debug(f"Watchers : {dict['Watchers']}")
            dict['Subscribers'] = repo.subscribers_count
            logger.debug(f"Subscribers : {dict['Subscribers']}")
            dict['Forks'] = repo.forks_count
            logger.debug(f"Forks : {dict['Forks']}")
            dict['Fork'] = repo.fork
            logger.debug(f"Fork : {dict['Fork']}")
            try:
                dict['License'] = repo.get_license().license.name
            except Exception as e:
                logger.error(e)
                dict['License'] = "NA"
            logger.debug(f"License : {dict['License']}")
            dict['Language'] = repo.language
            logger.debug(f"Language : {dict['Language']}")
            dict['Languages'] = repo.get_languages()
            logger.debug(f"Languages : {dict['Languages']}")
            dict['Creation date'] = repo.created_at.strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"Creation date : {dict['Creation date']}")
            try:
                dict['Modification date'] = repo.pushed_at.strftime("%Y-%m-%d %H:%M:%S")
                logger.debug(f"Modification date : {dict['Modification date']}")
            except Exception as e:
                logger.error(e)
                dict['Modification date'] = "NA"
            dict['Contributors'] = repo.get_contributors().totalCount
            logger.debug(f"Contributors : {dict['Contributors']}")
            dict['Topics'] = repo.get_topics()
            logger.debug(f"Topics : {dict['Topics']}")

            dict_repos[index] = dict
            dict_complete[index_complete] = dict
            index_complete += 1
        try:
            os.makedirs('Exports/')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        df = pd.DataFrame.from_dict(dict_repos, orient='index')
        df.to_csv(f"Exports/{user.login}-repos.csv", sep='\t')
    if not os.path.isfile("Exports/complete-user-repos.csv"):
        with open("Exports/complete-user-repos.csv", 'w') as f:
            f.write(f"User\tOwner\tName\tURL\tDescription\tStars\tWatchers\tSubscribers\tForks\tFork\tLicense\tLanguage\tLanguages\tCreation date\tModification date\tContributors\tTopics\n")
    with open("Exports/complete-user-repos.csv", 'a') as f:
        df = pd.DataFrame.from_dict(dict_complete, orient='index')
        df.to_csv(f, sep='\t', header=False)
    logger.info("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Repos information by user')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-u', '--user', help="Users to search (separated by comma)", type=str)
    parser.add_argument('-f', '--file', help="File containing the users (one by line)", type=str)
    parser.set_defaults(boolean_flag=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
