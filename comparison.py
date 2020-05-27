#Example of multithreading (comparison)

from threading import Thread    #pacote para fazer multithreading
from Queue import Queue         #estrutura de dados para fazer uso de multithreading
import logging                  #pacote para salvar logs do processamento
import time                     
import tqdm
import json

# processing for one instance
def process_one(q, results): # q -> queue, results-> optional argument to save some result
    while not q.empty():    # while q has instances to process
        val = q.get()       # get an instance 
        try:
            # time spent to process one instance
            time.sleep(0.1)
            # save thre result
            results.append(val)
        except Exception as e:
            print('if the instance was not processed, add to the queue again')
            q.put(val)
        #finish task
        q.task_done()
    return True

def process_threads(lista_in, num_threads):
    # set up the queue to hold all the instances of our data (lista_in)
    q = Queue(maxsize=0)
    print("number of instances: %s " %len(lista_in))
    pnum_threads = min(num_threads, len(lista_in))
    print("we use %s threads" %pnum_threads)
    results = []
    # add all instances to our list
    for i in range(len(lista_in)):
        q.put(lista_in[i])

    for j in range(pnum_threads): #use the number of threads passed as parameter
        logging.debug('Starting thread ', j)
        #create a new thread
        worker = Thread(target = process_one, args=(q, results))
        worker.setDaemon(True)
        worker.start()
    # now wait until the queue has been processed
    q.join()

    logging.info('All tasks completed')

    #save the results in a file
    with open('file_result_threading.json', 'w') as out:
        json.dump(results, out)

def process_sequential(lista_in, results):
    print("number of instances: %s " %len(lista_in))
    for val in tqdm.tqdm(lista):
        # time spent to process one instance
        time.sleep(0.1)
        results.append(val)

    #save results in a file
    with open('file_result_sequentail.json', 'w') as out:
        json.dump(results, out)

# create instances for the example
lista = []
for i in range(100):
    lista.append(i)

#process with the two options

print('#####################')
print('SEQUENTIAL OPTION')
results_seq = []
time_seq0 = time.time()
process_sequential(lista, results_seq)
time_seq1 = time.time()
print('It takes %f seconds to finish\n'%(time_seq1-time_seq0))

print('#####################')

print('MULTITHREADING OPTION - 50 Threads') 
results_threads = []
time_thread0 = time.time()
process_threads(lista, 50)
time_thread1 = time.time()
print('It takes %f seconds to finish\n'%(time_thread1-time_thread0))

print('#####################')

print('MULTITHREADING OPTION - 100 Threads') 
results_threads = []
time_thread0 = time.time()
process_threads(lista, 100)
time_thread1 = time.time()
print('It takes %f seconds to finish'%(time_thread1-time_thread0))


