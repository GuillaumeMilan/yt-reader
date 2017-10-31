from __future__ import print_function

# Print iterations progress
def printProgressBar (percent, prefix = '', suffix = '', decimals = 1, length = 100, fill = '='):
    """
    Call in a loop to create terminal progress bar
    @params:
        percent     - Required  : (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    filledLength = int(length * percent // 100)
    bar = fill * filledLength + ' ' * (length - filledLength)
    percent_str = str(percent)+"%"
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if percent == 100: 
        print()

# 
# Sample Usage
# 

##from time import sleep
#
## A List of Items
#items = list(range(0, 57))
#l = len(items)
#
## Initial call to print 0% progress
#printProgressBar(0, prefix = 'Progress:', suffix = 'Complete', length = 50)
#for i in range(1,101):
#    printProgressBar(i, prefix = 'Progress:', suffix = 'Complete', length = 50)
#    sleep(0.1)
#
