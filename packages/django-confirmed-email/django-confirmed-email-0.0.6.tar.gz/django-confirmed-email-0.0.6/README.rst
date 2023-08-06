======================
Confirmed Email Sender
======================

This package provides a drop-in replacements for shortcut send_mail() and class 
"EmailMultiAlternatives" which ensures that destination addresses are confirmed
before sending email to them.

The shortcut "send_mail_confirmed()" and class "ConfirmedEmailMessage" send email only
to confirmed addresses and automatically send confirmation messages to unconfirmed addresses.
It handles the confirmation process via a url in the confirmation message.

Messages for unconfirmed addresses will be queued until the address is confirmed
or a timeout period defaulting to 3 days elapses.

This app is configured with the same settings as Django's email backend plus
EMAIL_CONFIRMATION_WAIT which is an integer specifying the number of days to keep
queued messages for an unconfirmed address before deleting them.  This setting
defaults to 3.  You also need a valid domain name for Django's Sites framework
so the confirmation link is at the correct host.

If you're unfamiliar with the Sites framework, look for 'Sites' in the Django admin,
it should be self-explanatory.

ConfirmedEmailMessage.send() and send_email_confirmed() differ from the originals in
their return values.  Instead of a return value of 0/1 to indicate failure/success there
can be a different status for each destination address.   These return instead a dictionary with
each destination address as a key and a state indicating
success/failure/queued pending confirmation; see the documentation for
sender.ConfirmedEmailMessage.sent() for details.
This allows you to display a message indicating that confirmation is necessary if appropriate.

settings variables:

EMAIL_CONFIRMATION_WAIT: Number of days to wait between sending confirmation emails.
    Defaults to 3 days.

EMAIL_CONFIRMATION_TEMPLATE: Template to use as the body of confirmation emails.
    It's important for this template to contain a link for the user to click on
    passed to the template via variable {{confirmation_link}}.  See default template
    'confirmed_email/confirmation_email.txt' for an example.

ADDRESS_CONFIRMED_TEMPLATE: Template displayed to a user when they click on a confirmation link.
    Defaults to 'confirmed_email/address_confirmed.html' and has template variable
    {{email_address}} passed to it.

Example (view) usage:

    destination_address = 'noone@nowhere.com'
    cem = ConfirmedEmailMessage(
        subject='No Subject Needed',
        body='Hi there.',
        from_email='someservice@nowhere.com',
        to=[destination_address],
    )

    send_results = cem.send()
    if send_results[destination_address] == 'queued':
        template = 'confirmed_email/confirmation_required.html'
        context = {'email_address': destination_address}
        return render(request, template, context)
