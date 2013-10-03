from fabric.state import env

__author__ = 'john'

env.roledefs = {
    'production': ['enfortit@87.241.226.36'],
    'staging': ['enfortit@87.241.226.36']
}

import db
import deploy
import prepare_deployment
import provision