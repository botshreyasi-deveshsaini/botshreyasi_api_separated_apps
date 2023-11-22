from django.shortcuts import render
# from api.middleware import get_current_user
from django_currentuser.middleware import get_current_authenticated_user
from application.models import Application
from application.serializer import ApplicationSerializer
from django.conf import settings
import json
from django.db import connections, connection
from authorization.models import User
from django.http import JsonResponse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# with connections['my_db_alias'].cursor() as cursor:
from url_shortner.models import UrlShortners
from url_shortner.serializers import UrlShortnersSerializer
import re
import random
import secrets
from django.contrib.sites.models import Site


def getUser():
    user = vars(get_current_authenticated_user())
    del user['_state']
    return user


def GetUserID():
    user_id = get_current_authenticated_user().id
    return user_id


def GetApplication():
    application_id = get_current_authenticated_user().application_id
    try:
        application = ApplicationSerializer(
            Application.objects.get(id=application_id)).data
    except:
        print('No data Found')
    return application


def GetAppID():
    return get_current_authenticated_user().application_id


def MysqlCombineRowColumn(DBRow, DBcursor):
    DBColumn = [column[0]
                for column in DBcursor.description]
    DBResponse = []
    for event in DBRow:
        DBResponse.append(dict(zip(DBColumn, event)))
    return DBResponse


def MysqlCombineModelsRowColumn(RowName, ModelFields, ModelData):
    ColumnNames = [field.name for field in ModelFields if field.name != 'id']
    MergedData = {'Row Name': RowName, }
    for column in ColumnNames:
        if hasattr(ModelData, column):
            MergedData[column] = getattr(ModelData, column)
        else:
            MergedData[column] = None
    return MergedData


def can_be_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def GetStoreProcedureData(functions, params):
    # DBcursor = connections["mysqlslave"].cursor()
    with connections["mysqlslave"].cursor() as DBcursor:
        DBcursor.callproc(functions, params)
        DBRow = DBcursor.fetchall()
        return MysqlCombineRowColumn(DBRow, DBcursor)


def GetQueryData(DBqueary):
    # DBcursor = connections["mysqlslave"].cursor()
    with connections["mysqlslave"].cursor() as DBcursor:
        DBcursor.execute(DBqueary)
        DBRow = DBcursor.fetchall()
        return MysqlCombineRowColumn(DBRow, DBcursor)
    # DBColumn = [column[0]
    #     for column in DBcursor.description]
    # DBResponse = []
    # for event in DBRow:
    #     DBResponse.append(dict(zip(DBColumn, event)))
    # return DBResponse


def GetChild(application_id, self_id):
    all_users = User.objects.filter(application_id=application_id).order_by(
        'manager').values('id', 'manager')
    all_users_after = [dict(user) for user in all_users]
    all_role = {}
    for user in all_users_after:
        all_child = get_all_child(all_users_after, user['id'])
        all_role[user['id']] = all_child
    set_to_parent(all_role)
    return all_role[int(self_id)]


def GetChildWithSelf(app_id, user_id, is_comma_separated=False):

    # Define your get_child function accordingly
    childs = GetChild(app_id, user_id)
    childs.append(user_id)
    if is_comma_separated:
        return ','.join(map(str, childs))
    else:
        return childs


def get_all_child(arr, id):
    all_id = []
    for user in arr:
        if user['manager'] == id and user['id']:
            all_id.append(user['id'])
    return all_id


def set_all_data_to_key(all_ids, all_role):
    all_ids_temp = all_ids.copy()
    for index, value in enumerate(all_ids_temp):
        data = all_role[value]
        for val in data:
            if val not in all_ids:
                all_ids.append(val)
    return all_ids


def set_to_parent(all_role):
    for k1, v1 in all_role.items():
        current_id = k1
        for k, v in all_role.items():
            all_ids = all_role[current_id]
            # Pass all_role as an argument
            all_ids = set_all_data_to_key(all_ids, all_role)
            all_role[current_id] = all_ids


def StrReplace(string, array):
    for key, value in array.items():
        if isinstance(value, str):
            string = string.replace(f"[{key}]", value)
    return string


# def prepare_message(data, template):
#     print(data)
#     print(template)
#     for key, value in data:
#         template = template.replace(f'{{{key}}}', str(value))
#     return template
def prepare_message(data, template):
    for item in data:
        for key, value in item.items():
            template = template.replace(f'{{{key}}}', str(value))
    return template


# def generate_key(string, data):
#     # pattern = r'\[{(.*?)}\]'
#     print("genrate key ---------------->")
#     pattern = r'\*(.*?)\*'
#     print(string)
#     template = re.findall(pattern, string)
#     unique_template = list(set(template))
#     id=None
#     for link in unique_template:
#         random_key =  secrets.token_urlsafe(3)
#         chat_key =  secrets.token_urlsafe(32)
#         old_url = settings.SELF_DOMAIN + link
#         new_url = "b0t.in/"+ random_key
#         user_id = data[0].get('user_id', None)
#         Shortnersdata = {
#                     'url_key':random_key,
#                     'old_url':old_url,
#                     'chat_key':chat_key,
#                     'url_name' : "test",
#                     'user': user_id,
#                     'application' : data[0].get('application_id', None),
#                     'candidate' : data[0].get('candidate_id', None),
#                     'campaign_trigger' : data[0].get('campaign_trigger_id', None),
#                     'campaign' : data[0].get('campaign_id', None),
#         }
#         print(Shortnersdata)
#         ShortnersSerializer = UrlShortnersSerializer(data=Shortnersdata)
#         if ShortnersSerializer.is_valid():
#             UrlShortners_instance = ShortnersSerializer.save()
#             id = UrlShortners_instance.id
#         else:
#             print(ShortnersSerializer.errors)
#         string = string.replace(f"**{link}**", new_url)
#         id = UrlShortners_instance.id
#     data = {'template': string, 'urlshortner_id': id}
#     print(string)
#     return data



def generate_key(string, data,url_for):
    # Define the pattern to match text between '*'
    pattern = r'\*(.*?)\*'
    unique_template = list(set(re.findall(pattern, string)))
    ids =[]
    for link in unique_template:
        random_key = secrets.token_urlsafe(3)
        chat_key = secrets.token_urlsafe(32)
        old_url = settings.SELF_DOMAIN + link
        new_url = "b0t.in/" + random_key
        
        # Retrieve values from 'data' dictionary
        user_id = data[0]['user_id']
        application_id = data[0]['application_id']
        candidate_id = data[0]['candidate_id']
        campaign_trigger_id = data[0]['campaign_trigger_id']
        campaign_id = data[0]['campaign_id']
        campaign_trigger_history_id = data[0]['campaign_trigger_history_id']
        
        # Create a dictionary for UrlShortners data
        urlshortner_data = {
            'url_key': random_key,
            'old_url': old_url,
            'chat_key': chat_key,
            'url_name': "test",
            'user': user_id,
            'application': application_id,
            'candidate': candidate_id,
            'campaign_trigger': campaign_trigger_id,
            'campaign_trigger_history': campaign_trigger_history_id,
            'campaign': campaign_id,
            'url_for': url_for
        }
        
        # Serialize and save the UrlShortners data
        urlshortner_serializer = UrlShortnersSerializer(data=urlshortner_data)
        if urlshortner_serializer.is_valid():
            UrlShortners_instance = urlshortner_serializer.save()
            ids.append(UrlShortners_instance.id)
        else:
            print(urlshortner_serializer.errors)
        
        # Replace the link in the 'string' with the new URL
        string = string.replace(f"*{link}*", new_url)

    return {'template': string, 'urlshortner_id': ids}


def CalculateDatetimeInterval(value, unit):
    if unit == 'i':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    elif unit == 'm':
        return relativedelta(months=value)
    elif unit == 'y':
        # Approximate year interval (not accounting for leap years)
        return timedelta(days=365 * value)
    else:
        raise ValueError(
            "Invalid unit. Use 'i' for minutes, 'h' for hours, 'd' for days, 'm' for months, or 'y' for years.")
