from potentiostat import Potentiostat 
import matplotlib.pyplot as plt 
from time import sleep 

pstat = Potentiostat('/dev/ttyACM0') 
datafile = 'data.txt'

pstat.set_curr_range('100uA')
pstat.set_sample_rate(200.0) 

params = {
        'quietValue' : 0.0,
        'quietTime'  : 0,
        'step': [[20,0],[20,2.2]],
}
pstat.set_param('chronoamp',params)

for i in range(32000):
        t,volt,curr = pstat.run_test('chronoamp',display='data',filename=datafile)
        print(" current step - %" ,i) 
