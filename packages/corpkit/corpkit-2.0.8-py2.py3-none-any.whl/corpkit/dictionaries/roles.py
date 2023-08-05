# This file translates CoreNLP labels into SFL categories

def translator():
    from collections import namedtuple
    roledict = {
       'actor':          ['nsubj', 'agent', 'csubj', 'agent'],
       'adjunct':        ['advmod', 'agent', '(prep|nmod)(_|:).*', 'advcl', 'tmod'],
       'auxiliary':      ['auxpass', 'aux'],
       'circumstance':   ['advmod', r'(prep|nmod)(_|:).*', 'pobj', 'tmod'],
       'classifier':     ['compound', 'nn'],
       'complement':     ['acomp', 'dobj', 'iobj'],
       'deictic':        ['possessive', 'predet', 'poss', 'det', 'preconj'],
       'epithet':        ['amod'],
       'event':          ['ccomp', 'cop', 'advcl', 'root'],
       'existential':    ['expl'],
       'finite':         ['aux'],
       'goal':           ['nsubjpass', 'acomp', 'dobj', 'csubjpass', 'iobj'],
       'modifier':       ['advmod', 'amod', 'compound', 'nn', r'nmod.*', 'acl:relcl'],
       'premodifier':    ['amod', 'compound', 'nn', r'nmod'],
       'postmodifier':   [r'nmod:.*', 'acl:relcl'],
       'modal':          ['auxpass', 'aux'],
       'numerative':     ['number', 'quantmod'],
       'participant':    ['xsubj', 'nsubj', 'agent', 'nsubjpass', 'acomp', 
                          'csubj', 'dobj', 'appos', 'csubjpass', 'iobj', 'xcomp'],
       'participant1':   ['nsubj', 'agent', 'csubj'],
       'participant2':   ['nsubjpass', 'acomp', 'dobj', 'csubjpass', 'iobj', 'xcomp'],
       'polarity':       ['neg'],
       'predicator':     ['ccomp', 'cop', 'root'],
       'process':        ['ccomp', 'prt', 'cop', 'advcl', 'root', 'aux', 'auxpass'],
       'qualifier':      ['rcmod', 'vmod'],
       'subject':        ['nsubj', 'nsubjpass', 'csubj', 'csubjpass'],
       'textual':        ['cc', 'ref', 'mark'],
       'thing':          ['nsubj', 'agent', 'nsubjpass', 'csubj', 'dobj', 
                         r'(prep|nmod)(_|:).*', 'appos', 'csubjpass', 'pobj', 'iobj', 'tmod']}

    outputnames = namedtuple('roles', sorted([i for i in roledict.keys()]))
    return outputnames(*[sorted(roledict[w]) for w in outputnames._fields])

roles = translator()
