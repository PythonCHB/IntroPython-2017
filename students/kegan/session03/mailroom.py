#!/usr/bin/env python3

"""
Kathryn Egan

"""


DONORS = {
    'Benedict Cumberbatch': [200000.0],
    'Elon Musk': [10000.0, 150000.0, 100000.0],
    'Dad': [20.0, 5.0],
    'Donald Trump': [2.81],
    'Billy Neighbor': [.54, .01, .25]}

COLUMN_WIDTHS = [0] * 4


def main():
    """ Module that drives main menu."""
    options = {
        '1': {
            'prompt': 'Send a Thank You',
            'module': print_thank_you},
        '2': {
            'prompt': 'Create a Report',
            'module': print_report},
        '3': {
            'prompt': 'Quit',
            'module': exit_program}}
    while True:
        print('Please choose from the following options:')
        prompt = '\n'.join(['{} {}'.format(
            option, options[option]['prompt']) for option in options])
        answer = input(prompt + '\n>')
        if answer in options:
            options[answer]['module']()


def exit_program():
    """ Exits program and writes donor thank yous to files."""
    from sys import exit
    write_thank_yous()
    print('Exiting...')
    exit()


def print_thank_you():
    """ Prompts user for donor name and amount and prints thank
    you note to the console. Donation amount must be numerical."""
    while True:
        donor = input(
            'Who donated? (Enter LIST to see current list of donors)\n>')
        if donor.upper() != 'LIST':
            break
        print()
        print('Current donors:')
        print('\n'.join(sorted(DONORS)))
        print()
    donor = ' '.join(donor.split()).title()
    if donor not in DONORS:
        DONORS[donor] = []
    donation = get_donation()
    DONORS[donor].append(donation)
    thankyou = get_thank_you(donor, [donation])
    print(horizontal_line(80))
    print(thankyou)
    print(horizontal_line(80))


def get_donation():
    """ Prompts user for and returns donation amount.
    Returns:
        float : amount donated"""
    while True:
        donation = input('How much was donated?\n>')
        try:
            donation = float(donation.strip('$'))
            return donation
        except ValueError:
            print('{} is not a valid amount.'.format(donation))
            print('Please try again.')


def horizontal_line(length):
    """ Returns a horizontal line of given length.
    Args:
        length (int) : length of horizontal line
    Returns:
        str : horizontal line
    """
    return '-' * length


def get_thank_you(donor, donations):
    """ Returns a thank you message for the donor based
    off given donation if any, otherwise all donations
    in database.
    Args:
        donor (str) : name of donor
        donation (None or float) : specified donation
    Returns:
        str : thank you message for donor
    """
    total = sum(donations)
    num = len(donations)
    # build up elements of thank you message
    plural = 's' if num > 1 else ''
    plus = ' and ' if num > 1 else ''
    incredible = 'an incredible ' if total > 500 else ''
    totalling = ', totalling {}${},'.format(
        incredible, letter_dollar(total)) if num > 1 else ''
    message = \
        'Dear {},\nThank you for your '.format(donor) +\
        'generous gift{} of '.format(plural) + \
        ', '.join(['${}'.format(letter_dollar(d)) for d in donations[:-1]]) +\
        '{}${}. '.format(plus, letter_dollar(donations[-1])) +\
        'Your donation{}{} '.format(plural, totalling) +\
        'will go towards feeding homeless kittens in Seattle. ' +\
        'From the bottom of our hearts, we at Miuvenile Care thank you.\n\n' +\
        'Regards,\nBungelina Bigglesnorf\nChairwoman, Miuvenile Care'
    return message


def print_report():
    """ Prints a report showing donors and donation data to console."""
    headers = ('Donor Name', 'Total Given', 'Num Gifts', 'Average Gift')
    update_widths(headers)
    data = []
    # obtain data and determine ideal column lengths before making report
    for donor in sorted(DONORS, key=by_donation, reverse=True):
        donations = DONORS[donor]
        line = [donor, sum(donations), len(donations), average(donations)]
        update_widths(line)
        data.append(line)
    report = []
    report.append(stringify(headers, '| '))
    line_width = sum(COLUMN_WIDTHS) + len(COLUMN_WIDTHS) * 2 + 1
    report.append(horizontal_line(line_width))
    for row in data:
        report.append(stringify(row, ' '))
    print('\n' + '\n'.join(report) + '\n')


def update_widths(line):
    """ Updates minimum column widths based on
    the length of items (as strings) in given line.
    Args:
        line (list) : list of values
    """
    for index in range(len(line)):
        item = line[index]
        # dollar amounts are slightly longer in final report
        if type(item) is float:
            item = report_dollar(item)
        item = str(item)
        if len(item) > COLUMN_WIDTHS[index]:
            COLUMN_WIDTHS[index] = len(item)


def write_thank_yous():
    """ Writes thank yous to all donors in individual
    files in a ThankYous folder in the program's cwd."""
    import os
    print('Writing new thank yous to all donors...')
    for donor in DONORS:
        thankyou = get_thank_you(donor, DONORS[donor])
        if not os.path.exists('ThankYous'):
            os.makedirs('ThankYous')
        with open(os.path.join('ThankYous', donor + '.txt'), 'w') as f:
            f.write(thankyou)
    print('Thank yous written to\n{}'.format(
        os.path.join(os.getcwd(), 'ThankYous')))


def by_donation(donor):
    """ Returns the sum of the donations for given donor.
    Args:
        donor (str) : donor name
    Returns:
        float : sum of all donations for given donor
    """
    return sum(DONORS[donor])


def average(donations):
    """ Returns average of given donations rounded to 2 decimals.
    Args:
        donations (list of floats) : list of donations
    Returns:
        float : average of donations
    """
    avg = sum(donations) / len(donations)
    return round(avg, 2)


def report_dollar(amount):
    """ Returns amount in a format suitable for showing
    dollar amounts, e.g. 181.98.
    Args:
        amount (float) : amount to turn into dollar format
    Returns:
        str : amount in dollar format
    """
    dollars, cents = str(amount).split('.')
    if len(cents) == 1:
        cents += '0'
    return '.'.join([dollars, cents])


def letter_dollar(amount):
    """ Returns amount in a format suitable for showing
    dollar amounts, e.g. 181.98 or 211. Removes cents
    from any whole dollar amount.
     Args:
        amount (float) : amount to turn into dollar format
    Returns:
        str : amount in dollar format
    """
    if amount % 1 == 0:
        return str(int(amount))
    return report_dollar(amount)


def pad(string, length, trailing):
    """ Adds leading or trailing whitespace to a string
    up to a given total length. Orientation gives whether
    whitespace should be leading or trailing.
    Args:
        string (str) : string to pad with whitespace
        length (int) : desired length of string after padding
        trailing (str) :
            True if you want trailing whitespace
            False if you want leading whitespace
    Returns:
        str : string padded with whitespace
    """
    while len(string) < length:
        if trailing:
            string = string + ' '
        else:
            string = ' ' + string
    return string


def stringify(row, separator):
    """ Returns given row as a string.
    Args:
        row (list of str) : list of items in row
        separator (str) : separator for columns
    Returns:
        str : row as a string
    """
    line = []
    trailing = True  # trailing WS on first line
    for value, width in zip(row, COLUMN_WIDTHS):
        # monetary values get WS inserted between $ and number
        if type(value) is float:
            value = report_dollar(value)
            value = pad(value, width, trailing)
            value = '$' + value + ' '
        # numbers have leading WS with one extra WS in front and back
        elif type(value) is int:
            value = str(value)
            value = pad(value, width, trailing)
            value = ' ' + value + ' '
        # names having trailing WS with one extra WS
        else:  # str format
            value = pad(value, width, trailing)
            value += ' '  # WS cushion for both left/right columns
        trailing = False
        line.append(value)
    return separator.join(line).strip()


if __name__ == '__main__':
    main()
