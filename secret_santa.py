import yaml
# sudo pip install pyyaml
import re
import random
import smtplib
import datetime
import pytz
import time
import socket
import sys
import getopt
import os

help_message = '''
To use, fill out config.yml with your own participants. You can also specify 
DONT-PAIR so that people don't get assigned their significant other.

You'll also need to specify your mail server settings. An example is provided
for routing mail through gmail.

For more information, see README.
'''

REQRD = (
    'SMTP_SERVER', 
    'SMTP_PORT', 
    'USERNAME', 
    'PASSWORD', 
    'TIMEZONE', 
    'PARTICIPANTS', 
    'DONT-PAIR', 
    'FROM', 
    'SUBJECT', 
    'MESSAGE',
)

HEADER = """Date: {date}
Content-Type: text/plain; charset="utf-8"
Message-Id: {message_id}
From: {frm}
To: {to}
Subject: {subject}
        
"""

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')

class Person:
    def __init__(self, name, email, invalid_matches):
        self.name = name
        self.email = email
        self.invalid_matches = invalid_matches
    
    def __str__(self):
        return "%s <%s>" % (self.name, self.email)

class Pair:
    def __init__(self, giver, reciever):
        self.giver = giver
        self.reciever = reciever
    
    def __str__(self):
        return "%s ---> %s" % (self.giver.name, self.reciever.name)

def parse_yaml(yaml_path=CONFIG_PATH):
    return yaml.load(open(yaml_path))    

def choose_reciever(giver, recievers):
    choice = random.choice(recievers)
    if choice.name in giver.invalid_matches or giver.name == choice.name:
        if len(recievers) is 1:
            raise Exception('Only one reciever left, try again')
        return choose_reciever(giver, recievers)
    else:
        return choice

def create_pairs(g, r):
    givers = g[:]
    recievers = r[:]
    pairs = []
    for giver in givers:
        try:
            reciever = choose_reciever(giver, recievers)
            recievers.remove(reciever)
            pairs.append(Pair(giver, reciever))
        except:
            return create_pairs(g, r)
    return pairs


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "shc", ["send", "help"])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        send = False
        for option, value in opts:
            if option in ("-s", "--send"):
                send = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
                
        config = parse_yaml()
        for key in REQRD:
            if key not in config.keys():
                raise Exception(
                    'Required parameter %s not in yaml config file!' % (key,))

        participants = config['PARTICIPANTS']
        dont_pair = config['DONT-PAIR']
        if len(participants) < 2:
            raise Exception('Not enough participants specified.')
        
        givers = []
        for person in participants:
            name, email = re.match(r'([^<]*)<([^>]*)>', person).groups()
            name = name.strip()
            invalid_matches = []
            for pair in dont_pair:
                names = [n.strip() for n in pair.split(',')]
                if name in names:
                    # is part of this pair
                    for member in names:
                        if name != member:
                            invalid_matches.append(member)
            person = Person(name, email, invalid_matches)
            givers.append(person)
        
        recievers = givers[:]
        pairs = create_pairs(givers, recievers)
        if not send:
            print """
Test pairings:
                
%s
                
To send out emails with new pairings,
call with the --send argument:

    $ python secret_santa.py --send
            
            """ % ("\n".join([str(p) for p in pairs]))
        
        if send:
            server = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
            server.starttls()
            server.login(config['USERNAME'], config['PASSWORD'])
        for pair in pairs:
            zone = pytz.timezone(config['TIMEZONE'])
            now = zone.localize(datetime.datetime.now())
            date = now.strftime('%a, %d %b %Y %T %Z') # Sun, 21 Dec 2008 06:25:23 +0000
            message_id = '<%s@%s>' % (str(time.time())+str(random.random()), socket.gethostname())
            frm = config['FROM']
            to = pair.giver.email
            subject = config['SUBJECT'].format(santa=pair.giver.name, santee=pair.reciever.name)
            body = (HEADER+config['MESSAGE']).format(
                date=date, 
                message_id=message_id, 
                frm=frm, 
                to=to, 
                subject=subject,
                santa=pair.giver.name,
                santee=pair.reciever.name,
            )
            if send:
                result = server.sendmail(frm, [to], body)
                print "Emailed %s <%s>" % (pair.giver.name, to)

        if send:
            server.quit()
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())