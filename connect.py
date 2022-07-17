import gspread
from oauth2client.service_account import ServiceAccountCredentials

def initGspreadClient():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "token.json", scope)
    client = gspread.authorize(creds)
    return client