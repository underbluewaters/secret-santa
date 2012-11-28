Intro
=====

**secret-santa** can help you manage a list of secret santa participants by
randomly assigning pairings and sending emails. It can avoid pairing 
couples to their significant other, and allows custom email messages to be 
specified.

Dependencies
------------

pytz
pyyaml

Usage
-----

Copy config.yml.template to config.yml and enter in the connection details 
for your outgoing mail server. Modify the participants and couples lists and 
the email message if you wish.

    cd secret-santa/
    cp config.yml.template config.yml

Here is the example configuration unchanged:

    # Required to connect to your outgoing mail server. Example for using gmail:
    # gmail
    SMTP_SERVER: smtp.gmail.com
    SMTP_PORT: 587
    USERNAME: you@gmail.com
    PASSWORD: "you're-password"

    TIMEZONE: 'US/Pacific'

    PARTICIPANTS:
      - Chad <chad@somewhere.net>
      - Jen <jen@gmail.net>
      - Bill <Bill@somedomain.net>
      - Sharon <Sharon@hi.org>

    # Warning -- if you mess this up you could get an infinite loop
    DONT-PAIR:
      - Chad, Jen    # Chad and Jen are married
      - Chad, Bill   # Chad and Bill are best friends
      - Bill, Sharon

    # From address should be the organizer in case participants have any questions
    FROM: You <you@gmail.net>

    # Both SUBJECT and MESSAGE can include variable substitution for the 
    # "santa" and "santee"
    SUBJECT: Your secret santa recipient is {santee}
    MESSAGE: 
      Dear {santa},

      This year you are {santee}'s Secret Santa!. Ho Ho Ho!

      The maximum spending limit is 50.00


      This message was automagically generated from a computer. 

      Nothing could possibly go wrong...

      http://github.com/underbluewaters/secret-santa

Once configured, call secret-santa:

    python secret_santa.py

Calling secret-santa without arguments will output a test pairing of 
participants.

        Test pairings:

        Chad ---> Bill
        Jen ---> Sharon
        Bill ---> Chad
        Sharon ---> Jen

        To send out emails with new pairings,
        call with the --send argument:

            $ python secret_santa.py --send

To send the emails, call using the `--send` argument

    python secret_santa.py --send