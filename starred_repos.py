import logging
import time
import argparse
import configparser
import os
import errno
import pandas as pd
from github import Github
from tqdm import tqdm

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    username = args.user

    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['github']['username']
    password = config['github']['password']

    g = Github(username, password)

    user = g.get_user(username)
    starred_repos = user.get_starred()
    dict_repos = {}

    for index, repo in tqdm(enumerate(starred_repos, 1), total=starred_repos.totalCount, dynamic_ncols=True):
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
        dict['Modification date'] = repo.pushed_at.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Modification date : {dict['Modification date']}")
        try:
            dict['Contributors'] = repo.get_contributors().totalCount
            logger.debug(f"Contributors : {dict['Contributors']}")
        except Exception as e:
            logger.error(e)
            dict['Contributors'] = "NA"
        dict['Topics'] = repo.get_topics()
        logger.debug(f"Topics : {dict['Topics']}")

        dict_repos[index] = dict

    try:
        os.makedirs('Exports/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    df = pd.DataFrame.from_dict(starred_repos, orient='index')
    df.to_csv(f"Exports/{user.login}-starred-repos.csv", sep='\t')
    logger.info("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Get github starred repos')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-u', '--user', help="User (default : user logged by the config file)", type=str)
    parser.set_defaults(boolean_flag=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
