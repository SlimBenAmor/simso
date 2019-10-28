#!/usr/bin/python3

"""
Example of a script that uses SimSo.
"""

import sys
from simso.core import Model
from simso.configuration import Configuration
import numpy as np



def main(argv):
    if len(argv) == 2:
        # Configuration load from a file.
        configuration = Configuration(argv[1])
    else:
    
   
        # Manual configuration:
        configuration = Configuration()

        configuration.duration = 200 * configuration.cycles_per_ms
        
        g1= np.array([[0,1],
                      [0,0]])
        g2= np.array([[0,1,1,0,1,0],
                        [0,0,0,1,0,0],
                        [0,0,0,1,0,0],
                        [0,0,0,0,0,1],
                        [0,0,0,0,0,1],
                        [0,0,0,0,0,0]])

        c1=[8,10]
        c2=[1,1,2,2,7,2]

        p1=[1,2]
        p2=[1,1,2,2,1,2]

        T1 = 40 
        T2 = 50 

        sub_prio1=[1,2]
        sub_prio2=[1,3,4,5,2,6]
        
        # Add tasks:
        configuration.add_task(name="T1", identifier=1, task_type="DAG", period=T1,
        activation_date=0, wcet=c1, deadline=T1, precedence_matrix=g1, cpu_map=p1,prio=1, sub_prio=sub_prio1)
        configuration.add_task(name="T2", identifier=2, task_type="DAG", period=T2,
        activation_date=0, wcet=c2, deadline=T2, precedence_matrix=g2, cpu_map=p2,prio=2, sub_prio=sub_prio2)
        
        
        # Add a processor:
        configuration.add_processor(name="CPU 1", identifier=1)
        configuration.add_processor(name="CPU 2", identifier=2)
        
        # Add a scheduler:
        configuration.scheduler_info.clas = "simso.schedulers.P_FP_sub"
        
        # Check the config before trying to run it.
        configuration.check_all()
    
        # Init a model from the configuration.
        model = Model(configuration)
    
        # Execute the simulation.
        model.run_model()
            
        # Print logs.
        for log in model.logs:
            print(log)
           
    
main(sys.argv)
