Intro
=====

*secret-santa* can help you manage a list of secret santa participants by
randomly assigning pairings and sending emails. It can also avoid pairing 
couples to their significant other.

Usage
-----

Copy config.yml.template to config.yml and enter in the connection details 
for your outgoing mail server. Modify the participants and couples lists and 
the email message if you wish.

Once configured, call secret-santa:

    cd secret-santa/
    cp config.yml.template config.yml
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

To send the emails, call using the (`--send`) argument

    python secret_santa.py --send