import boto3
import os
import random
import time
import decimal

# ---------------- Environment Variables ----------------
OTP_TABLE = os.environ.get('OTP_TABLE', '<YOUR_OTP_TABLE_NAME>')
FROM_EMAIL = os.environ.get('FROM_EMAIL', '<YOUR_EMAIL>')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', '<RECEIVER_EMAIL>')

# ---------------- AWS Resources ----------------
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='ap-southeast-2')

# ---------------- Helper Functions ----------------
def random_num():
    return decimal.Decimal(random.randrange(1000, 50000)) / 100

def get_slots(event):
    return event['sessionState']['intent'].get('slots', {})

def get_slot(event, name):
    s = get_slots(event)
    if s and name in s and s[name] is not None:
        return s[name]['value']['interpretedValue']
    return None

def get_session(event):
    return event['sessionState'].get('sessionAttributes', {})

def elicit(event, sess, slot, msg):
    intent = event['sessionState']['intent']
    intent['state'] = "InProgress"
    return {
        'sessionState': {
            'dialogAction': {'type': 'ElicitSlot', 'slotToElicit': slot},
            'sessionAttributes': sess,
            'intent': intent
        },
        'messages': [msg],
    }

def close(event, sess, state, msg):
    intent = event['sessionState']['intent']
    intent['state'] = state
    return {
        'sessionState': {
            'sessionAttributes': sess,
            'dialogAction': {'type': 'Close'},
            'intent': intent
        },
        'messages': [msg],
    }

# ---------------- OTP Functions ----------------
def generate_otp(email=RECEIVER_EMAIL):
    otp = str(random.randint(100000, 999999))
    expires = int(time.time()) + 300  # OTP valid for 5 minutes
    dynamodb.Table(OTP_TABLE).put_item(Item={'email': email, 'otp': otp, 'expires_at': expires})
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': 'Your BankingBot OTP'},
            'Body': {'Text': {'Data': f'Your OTP is {otp}. It expires in 5 minutes.'}}
        }
    )
    return otp

def verify_otp(email, otp_input):
    table = dynamodb.Table(OTP_TABLE)
    res = table.get_item(Key={'email': email})
    if 'Item' not in res:
        return False, "No OTP found. Please request a new one."
    item = res['Item']
    if int(time.time()) > item['expires_at']:
        return False, "OTP expired. Please request again."
    if otp_input != item['otp']:
        return False, "Invalid OTP. Please try again."
    table.delete_item(Key={'email': email})
    return True, "OTP verified."

# ---------------- OTP Handling ----------------
def handle_otp(event, sess, otp_slot='otp'):
    otp_input = get_slot(event, otp_slot)
    user_input = event.get('inputTranscript', '').lower()
    table = dynamodb.Table(OTP_TABLE)
    attempts = int(sess.get('otp_attempts', 0))
    max_attempts = 3

    existing_otp_item = table.get_item(Key={'email': RECEIVER_EMAIL}).get('Item')
    otp_valid = existing_otp_item and int(time.time()) <= existing_otp_item['expires_at']

    # Generate OTP if not sent or user requests resend
    if otp_input is None or 'resend' in user_input or not otp_valid:
        generate_otp()
        sess['otp_attempts'] = "0"
        msg = {'contentType': 'PlainText', 'content': f"📩 Sending a new OTP to {RECEIVER_EMAIL}. Please check your email ✉️ and enter it here."}
        return elicit(event, sess, otp_slot, msg)

    # Verify OTP
    ok, txt = verify_otp(RECEIVER_EMAIL, otp_input)
    if not ok:
        attempts += 1
        sess['otp_attempts'] = str(attempts)
        if attempts >= max_attempts:
            sess['otp_attempts'] = "0"
            generate_otp()
            msg = {'contentType': 'PlainText', 'content': "✖️ Incorrect OTP 3 times. Sending a new OTP 📩. Try again."}
            return elicit(event, sess, otp_slot, msg)
        else:
            msg = {'contentType': 'PlainText', 'content': f"😕 {txt} You have {max_attempts - attempts} attempt(s) left. (Type 'resend' to get a new OTP 📩.)"}
            return elicit(event, sess, otp_slot, msg)

    # OTP verified successfully
    sess['otp_attempts'] = "0"
    return None

# ---------------- Intents ----------------
def CheckBalance(event):
    sess = get_session(event)
    otp_response = handle_otp(event, sess)
    if otp_response: return otp_response
    bal = str(random_num())
    msg = {'contentType': 'PlainText', 'content': f"🏦 Your account balance is ${bal} 💰."}
    return close(event, sess, "Fulfilled", msg)

def Payment(event):
    sess = get_session(event)
    otp_response = handle_otp(event, sess)
    if otp_response: return otp_response
    account = get_slot(event, 'accountType') or "your account"
    amount = get_slot(event, 'amount') or "an amount"
    msg = {'contentType': 'PlainText', 'content': f"💸 Payment of ${amount} from {account} completed successfully 💰."}
    return close(event, sess, "Fulfilled", msg)

def Transfer(event):
    sess = get_session(event)
    otp_response = handle_otp(event, sess)
    if otp_response: return otp_response
    from_acc = get_slot(event, 'fromAccount') or "source account"
    to_acc = get_slot(event, 'toAccount') or "destination account"
    amount = get_slot(event, 'amount') or "an amount"
    msg = {'contentType': 'PlainText', 'content': f"💸 ${amount} transferred from {from_acc} to {to_acc} successfully 💰."}
    return close(event, sess, "Fulfilled", msg)

def ThankYou(event):
    sess = get_session(event)
    msg = {'contentType': 'PlainText', 'content': "You're welcome! 😊"}
    return close(event, sess, "Fulfilled", msg)

# ---------------- Dispatch ----------------
def dispatch(event):
    name = event['sessionState']['intent']['name']
    if name == 'CheckBalance': return CheckBalance(event)
    if name == 'Payment': return Payment(event)
    if name == 'Transfer': return Transfer(event)
    if name == 'ThankYou': return ThankYou(event)
    raise Exception(f"Unsupported intent: {name}")

# ---------------- Lambda Handler ----------------
def lambda_handler(event, context):
    return dispatch(event)
