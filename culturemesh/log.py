import logging

def log_home():
    logging.basicConfig(filename='data/logging/homepagevisits.log', level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s at %(asctime)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('Visits')

def new_user():
    logging.basicConfig(filename='data/logging/users.log', level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s at %(asctime)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('User Number: ')
