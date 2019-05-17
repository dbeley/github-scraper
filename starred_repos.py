import logging
import time
import argparse
import configparser
import pandas as pd
from github import Github
from tqdm import tqdm
from pathlib import Path

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()

    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['github']['username']
    password = config['github']['password']

    if args.user:
        username = args.user

    g = Github(username, password)

    user = g.get_user(username)
    starred_repos = user.get_starred()
    dict_repos = {}

    for index, repo in tqdm(enumerate(starred_repos, 1), total=starred_repos.totalCount, dynamic_ncols=True):
        dict = {}
        dict['User'] = user.login
        logger.debug("User : %s", dict['User'])
        dict['Owner'] = repo.owner.login
        logger.debug("Owner : %s", dict['Owner'])
        dict['Name'] = repo.name
        logger.debug("Name : %s", dict['Name'])
        dict['URL'] = repo.html_url
        logger.debug("URL : %s", dict['URL'])
        dict['Description'] = repo.description
        logger.debug("Description : %s", dict['Description'])
        dict['Stars'] = repo.stargazers_count
        logger.debug("Stars : %s", dict['Stars'])
        dict['Subscribers'] = repo.subscribers_count
        logger.debug("Subscribers : %s", dict['Subscribers'])
        dict['Forks'] = repo.forks_count
        logger.debug("Forks : %s", dict['Forks'])
        dict['Fork'] = repo.fork
        logger.debug("Fork : %s", dict['Fork'])
        try:
            dict['License'] = repo.get_license().license.name
        except Exception as e:
            logger.error(e)
            dict['License'] = "NA"
        logger.debug("License : %s", dict['License'])
        dict['Language'] = repo.language
        logger.debug("Language : %s", dict['Language'])
        dict['Languages'] = repo.get_languages()
        logger.debug("Languages : %s", dict['Languages'])
        dict['Creation date'] = repo.created_at.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug("Creation date : %s", dict['Creation date'])
        dict['Modification date'] = repo.pushed_at.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug("Modification date : %s", dict['Modification date'])
        try:
            dict['Contributors'] = repo.get_contributors().totalCount
            logger.debug("Contributors : %s", dict['Contributors'])
        except Exception as e:
            logger.error(e)
            dict['Contributors'] = "NA"
        dict['Topics'] = repo.get_topics()
        logger.debug("Topics : %s", dict['Topics'])

        dict_repos[index] = dict

    Path("Exports").mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame.from_dict(dict_repos, orient='index')
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
