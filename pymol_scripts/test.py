# import re
#
# stri = '*out'
# test = ['out', 'aaout', 'sdfgsdg']
#
# regex = re.compile('%s*' % stri)
# # print regex


user = '*out'
import re
regex = re.compile('%s-\d*' % user)
regex.match('heinz-1')
print regex