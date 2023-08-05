#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals
import codecs

from colorama import init, Fore, Style
import pyperclip
import os, sys
import scrypt
import json
import math

# Fixes getpass bug that affects python 2.7 on windows
# credit to https://bitbucket.org/ZyX_I/gibiexport/commits/a1241335fe53
if sys.version_info < (3,) and sys.platform.startswith('win'):
    from getpass import getpass as _getpass
    def getpass(s):
        try:
            return _getpass(str(s))
        except UnicodeEncodeError:
            from locale import getpreferredencoding
            try:
                return _getpass(s.encode(getpreferredencoding()))
            except UnicodeEncodeError:
                return _getpass(b'Master password: ')
else:
    from getpass import getpass

# Initialise colours for multi-platform support.
init()

# Initialise input for multi-version support.
try:
    input = raw_input
except NameError:
    pass


def generate(master_password, keyword, cost=14, oLen=32):
    hashed = scrypt.hash(
        password = master_password,
        salt = keyword,
        N = 1 << cost,
        buflen=32
    )
    return codecs.encode(hashed, 'hex').decode('utf-8')[0:oLen]


def generate_readable(generated):
    with open('%s/words.txt' % path, 'rb') as f:
        words = f.read().splitlines()
    dict_len = len(words)
    entropy_per_word = math.log(dict_len, 2)
    maximum_desired_entropy = int(math.ceil(params['nwords'] * math.log(dict_len, 2)))
    num_words = int(math.ceil(maximum_desired_entropy // entropy_per_word))
    hash = codecs.encode(scrypt.hash(str(generated), b'', N=1 << 14), 'hex').decode('utf-8')
    available_entropy = len(hash) * 4
    hash = int(hash, 16)
    if (num_words * entropy_per_word) > available_entropy:
        raise Exception("The output entropy of the specified hashfunc (%d) is too small." % available_entropy)
    phrase = []
    for i in range(num_words):
        remainder = hash % dict_len
        hash = hash / dict_len
        phrase.append(words[int(remainder)].strip().decode('utf-8'))
    return " ".join(phrase).lower().capitalize()


def copy_to_clipboard(generated):
    global copied
    selection = safe_input('Which password would you like to copy? (1/2) ').strip()
    if selection == '1':
        password = generated[0]
    elif selection == '2':
        password = generated[1]
    else:
        print(err('Invalid option. Pick either 1 or 2.\n'))
        return copy_to_clipboard(generated)
    try:
        pyperclip.copy(password)
        copied = True
        print('\nCopied!\n')
        return
    except pyperclip.exceptions.PyperclipException:
        print(err('Could not copy! If you\'re using linux, make sure xclip is installed.\n'))


def err(text):
    return '%s%s%s' % (Fore.RED, text, Fore.RESET)


def settings(text):
    return '%s%s%s' % (Fore.YELLOW, text, Fore.RESET)


def password(text):
    return '%s%s%s' % (Fore.CYAN, text, Fore.RESET)


def safe_input(string):
    try:
        return str(input(string))
    except EOFError:
        print(err('Input unusable.\n'))
        return safe_input(string)


def exit_protocol(msg=''):
    if copied:
        pyperclip.copy('')
    if msg:
        print(err('\n' + msg))
    print(err('\nExiting securely... You are advised to close this terminal.'))
    raise SystemExit


def get_defaults():
    print('\nEnter your preferred settings: (leave blank to accept defaults)\n')
    cost = safe_input('Cost factor as a power of 2 [default=14]: ')
    if cost:
        if cost.isdigit():
            cost = int(cost)
            if cost < 10 or cost > 24:
                print(err('Input must be a positive integer between 10 and 24.\n'))
                return get_defaults()
        else:
            print(err('Input must be a positive integer between 10 and 24.\n'))
            return get_defaults()
    else:
        cost = 14
    oLen = safe_input('Length of generated passwords [default=32]: ')
    if oLen:
        if oLen.isdigit():
            oLen = int(oLen)
            if oLen > 64 or oLen < 16:
                print(err('Input must be a positive integer between 16 and 64.\n'))
                return get_defaults()
        else:
            print(err('Input must be a positive integer between 16 and 64.\n'))
            return get_defaults()
    else:
        oLen = 32
    nwords = safe_input('Number of words in a readable password [default=6]: ')
    if nwords:
        if nwords.isdigit():
            nwords = int(nwords)
            if nwords > 16 or oLen < 4:
                print(err('Input must be a positive integer between 4 and 16.\n'))
                return get_defaults()
        else:
            print(err('Input must be a positive integer between 4 and 16.\n'))
            return get_defaults()
    else:
        nwords = 6
    print() # line break for formatting
    return {"cost" : cost, "oLen" : oLen, "nwords" : nwords}


def getPath():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except:
        exit_protocol('ERROR: Cannot get path. Are you sure you\'re not running Visionary from IDLE?')


def getConfig():
    try:
        with open('%s/visionarypm.conf' % path) as f:
            config = json.loads(f.read().strip())
        if config['oLen'] < 16 or config['oLen'] > 64 or config['cost'] < 10 or config['cost'] > 24 or config['nwords'] > 16 or config['nwords'] < 4:
            exit_protocol('Invalid config! Please delete the configuration file (%s) and a new one will be generated on the next run.' % (path + '/visionarypm.conf'))
        return config, 0
    except IOError:
        config = get_defaults()
        autosave = safe_input('Do you want to save this config? (Y/n) ').lower()
        if autosave == 'yes' or autosave == 'y' or autosave == '':
            print('\nAutosaving configuration...')
            try:
                with open('%s/visionarypm.conf' % path, 'a') as f:
                    f.write(json.dumps(config))
                return config, 0
            except:
                print(err('Autosaving failed! (Permission denied)\n'))
                print('In order to save these settings, place %s' % settings(json.dumps(config)))
                print('in %s' % (settings('%s/visionarypm.conf' % path)))
        return config, 1
    except KeyError:
        exit_protocol('Invalid config! Please delete the configuration file (%s) and a new one will be generated on the next run.' % (path + '/visionarypm.conf'))


# Global parameters
params = {}
path = getPath()
copied = False


def interactive(first_run=True):
    if first_run == True:
        print("""%s%s
                        _     _
                 /\   /(_)___(_) ___  _ __   __ _ _ __ _   _
                 \ \ / / / __| |/ _ \| '_ \ / _` | '__| | | |
                  \ V /| \__ \ | (_) | | | | (_| | |  | |_| |
                   \_/ |_|___/_|\___/|_| |_|\__,_|_|   \__, |
                                       Password Manager|___/\n
        """ % (Fore.WHITE, Style.BRIGHT)) # Set global default colours.
        print(settings('  Please report any issues at https://github.com/libeclipse/visionary/issues'))
        global params
        params, stat = getConfig()
        if stat == 0:
            print("""
[+] Cost factor: 2^%s
[+] Length of conventional password: %s
[+] Words in readable password: %s
[+] Config file: %s""" % (settings(params['cost']),
                          settings(params['oLen']),
                          settings(params['nwords']),
                          settings('%s/visionarypm.conf' % path)))
    print() # line break for formatting
    master_password = getpass('Master password: ')
    master_password_confirm = getpass('Confirm master password: ')
    while master_password != master_password_confirm:
        print(err('Passwords don\'t match!\n'))
        master_password = getpass('Master password: ')
        master_password_confirm = getpass('Confirm master password: ')
    if len(master_password) >= 8:
        print() #line break for formatting
        while True:
            keyword = safe_input('Keyword: ')
            if keyword:
                # Generate password
                conventional = generate(master_password,
                                        keyword,
                                        params['cost'],
                                        params['oLen'])
                readable = generate_readable(conventional)
                generated = [conventional, readable]
                print('\n[%s] Conventional password: %s' % (settings('1'), password(generated[0])))
                print('[%s] Readable password: %s\n' % (settings('2'), password(generated[1])))
                # Copy to clipboard
                confirm = safe_input('Would you like to copy a password to the clipboard? (Y/n) ').lower().strip()
                if confirm == 'yes' or confirm == 'y' or confirm == '':
                    copy_to_clipboard(generated)
                else:
                    print() # line break for formatting
            else:
                exit_protocol()
                raise SystemExit
    else:
        print(err('Password must be at least 8 characters.\n'))
        interactive(False)


def main():
    try:
        interactive()
    except KeyboardInterrupt:
        exit_protocol('\nKeyboard Interrupt')
    except Exception as e:
        exit_protocol('ERROR: %s\n\nPlease report this error at https://github.com/libeclipse/visionary/issues' % str(e))


if __name__ == "__main__":
    main()
