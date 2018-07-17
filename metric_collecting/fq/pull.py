# -*- coding: utf-8 -*

import ConfigParser
import git
import helper
import pymysql
import csv

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

conn = pymysql.connect(host=cf.get("DB","host"),
                       port=int(cf.get("DB","port")),
                       user=cf.get("DB","user"),
                       passwd=cf.get("DB","password"),
                       db=cf.get("DB","database"),
                       charset='utf8')

def gitPull(repoPullDir):
    repo = git.Repo(repoPullDir)
    o = repo.remotes.origin
    o.pull()


def PullProcess():
    repoListFile = cf.get("server", "repoList")
    with open(repoListFile,"r") as f:
        reader = csv.reader(f,delimiter = ",")
        for item in reader:
            proName,repoName,gitAddr = item
            gitPull(cf.get("server","gitCloneAddr")+repoName)
