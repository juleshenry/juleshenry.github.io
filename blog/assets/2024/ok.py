z = '''
back-propagation.png
feed-forward-lstm.png
bidirectional-rnn.png
formulae.png
computation-graph.png
lstm-cell.svg
example.png
lstm.png
example2.png
rnn-notation.png
example3.png
unrolled-rnn.png
feed-backward-lstm.png
vanilla-forward-pass.png
'''
for o in z.split('\n'):
    if o:
        print(f"![{o.split('.')[0]}](/blog/assets/2024/{o}")
        
