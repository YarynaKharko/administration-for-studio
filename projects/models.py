
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import pymysql
from transliterate import translit
import re


class Project(models.Model):
    project_name = models.CharField(max_length=220)
    project_description = models.TextField()
    project_text = models.TextField()
    project_main_image = models.ImageField()
    #project_main_image = models.CharField(max_length=220)
    portfolio = models.TextField(default='image.png')

    def publish(self):
        self.save()

    def save(self, *args, **kwargs):
        list_portf = re.findall(r"\w+.\w+", self.portfolio)
        self.proj_url = Utiles.translate_to_latin(self.project_name)
        proj1 = Project_DB(project_name=self.project_name,
                           project_text=self.project_text,
                           project_description=self.project_description,
                           project_main_image=self.project_main_image)
        for image in list_portf:
            proj1.add_portfolio(Portfolio_DB(portfolio_image=image, proj_id=self.proj_url))
        Services.insert_project_to_db(proj1)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.project_name.encode('utf8')



class Utiles(object):
    @staticmethod
    def translate_to_latin(text, language_code='ru'):
        trans = list(translit(text, language_code, reversed=True))
        for i in range(len(trans)):
            if trans[i] == " " or trans[i] == "(" or trans[i] == ")":
                trans[i] = u"-"
            if trans[i] == "'":
                trans[i] = ""

        return ''.join(trans)

    @staticmethod
    def get_DB_connection(connection=None):
        DB_data = {
            'pyuser': {'host': '77.120.115.197',
                        'user': 'pyuser',
                        'passwd': '12345678',
                        'db': 'chartev4638'},
            'local': {'host': 'localhost',
                       'user': 'root',
                       'passwd': '25263004',
                       'db': 'DESIGN_STUDIO'},
            'default': {'host': '77.120.115.197',
                       'user': 'pyuser',
                       'passwd': '12345678',
                       'db': 'chartev4638'}
        }
        if connection is None:
            connection = 'default'
        if DB_data.has_key(connection):
            conn = pymysql.connect(host=DB_data[connection]['host'],
                                   port=3306,
                                   user=DB_data[connection]['user'],
                                   passwd=DB_data[connection]['passwd'],
                                   db=DB_data[connection]['db'], charset='utf8')
        return conn


class Project_DB(object):
    def __init__(self, id_proj=None, project_name=None, project_description=None, project_text=None,
                 project_main_image=None):
        self.id_proj = id_proj
        self.project_name = project_name
        self.project_description = project_description
        self.project_text = project_text
        self.project_main_image = project_main_image
        if not project_name == None:
            self.proj_url = Utiles.translate_to_latin(project_name)
        else: self.proj_url = None
        self.project_portfolio = list()
        #self.add_portfolio(project_portfolio)

    def add_portfolio(self, project_portfolio):
        if isinstance(project_portfolio, list):
            self.project_portfolio = project_portfolio
        elif isinstance(project_portfolio, Portfolio_DB):
            self.project_portfolio.append(project_portfolio)
        else: self.project_portfolio = None


class Portfolio_DB(object):
    def __init__(self, portfolio_image, proj_id, id_portfolio=None):
        self.id_portfolio = id_portfolio
        self.portfolio_image = portfolio_image
        self.proj_id = proj_id

queries_proj = {
        'insert': "INSERT INTO projects (proj_title,proj_text,proj_description,proj_main_image,proj_url) VALUES ('%s', '%s', '%s', '%s', '%s');"
    }
queries_portfolio = {
        'insert': "INSERT INTO portfolio (image, id_proj) VALUES ('%s', '%s');"
    }


class Services(object):

    @staticmethod
    def insert_project_to_db(project, connection=None):
        if isinstance(project, Project_DB):
            conn = Utiles.get_DB_connection(connection)
            cur = conn.cursor()
            cur.execute('SET SESSION CHARACTER_SET_RESULTS =utf8;')
            cur.execute('SET SESSION CHARACTER_SET_CLIENT =utf8;')
            query = queries_proj['insert'] % (unicode(project.project_name),
                                              unicode(project.project_text),
                                              unicode(project.project_description),
                                              unicode(project.project_main_image),
                                              project.proj_url,)
            result = cur.execute(query)
            print "EXECUTE MYSQL QUERY : ", query, 'result = ', result
            Services.insert_portfolio_to_db(project.project_portfolio, cursor=cur)

            cur.close()
            conn.commit()
            conn.close()

    @staticmethod
    def insert_portfolio_to_db(portfolio, cursor=None, connection=None):
        if portfolio is not None:
            if cursor is None:
                print 'INFORMATION : Cursore is None. Create and open new connection.'
                conn = Utiles.get_DB_connection(connection)
                cursor = conn.cursor()
                print 'CONNECTION INFORMATION : host :', cursor.connection.host, \
                    '\nuser : ', cursor.connection.user
                cursor.execute('SET SESSION CHARACTER_SET_RESULTS =utf8;')
                cursor.execute('SET SESSION CHARACTER_SET_CLIENT =utf8;')
                if isinstance(portfolio, Portfolio_DB):
                    query = queries_portfolio['insert'] % (portfolio.portfolio_image, portfolio.proj_id,)
                    result = cursor.execute(query)
                    print "EXECUTE MYSQL QUERY : ", query, 'result = ', result
                elif isinstance(portfolio, list):
                    for each in portfolio:
                        query = queries_portfolio['insert'] % (each.portfolio_image, each.proj_id,)
                        result = cursor.execute(query)
                        print "EXECUTE MYSQL QUERY : ", query, 'result = ', result
                cursor.close()
                conn.commit()
                conn.close()
            else:
                print 'Cursore is not None. Use cursore that passed into.'
                if isinstance(portfolio, Portfolio_DB):
                    query = queries_portfolio['insert'] % (portfolio.portfolio_image, portfolio.proj_id,)
                    result = cursor.execute(query)
                    print "EXECUTE MYSQL QUERY : ", query, 'result = ', result
                elif isinstance(portfolio, list):
                    for each in portfolio:
                        query = queries_portfolio['insert'] % (each.portfolio_image, each.proj_id,)
                        result = cursor.execute(query)
                        print "EXECUTE MYSQL QUERY : ", query, 'result = ', result
        else:
            print 'WARNING : Portfolio is None element. Cannot insert None element to DB.'