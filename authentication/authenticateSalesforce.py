from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
load_dotenv()

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
security_token = os.getenv("SECURITY_TOKEN")

sf = Salesforce(username=username, password=password, security_token=security_token)
