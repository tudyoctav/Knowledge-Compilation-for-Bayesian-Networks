import sys 
sys.path.append('./')

from KnowledgeCompilers.dimacs_parser import parse
from KnowledgeCompilers.dtree_compiler import Dtree_Compiler
from KnowledgeCompilers.graph_utils import export_dot_from_bdd
from KnowledgeCompilers.obdd_compiler import BDD_Compiler
from KnowledgeCompilers.dnnf_compiler import *
from KnowledgeCompilers.graph_utils import *
import copy
from pathlib import Path
import time
def generate_theory_from_cnf(filename,encoding='enc1'):
    cnf_file = f'demo_instances/{filename}/{encoding}_dimacs.cnf'
    clausal_form, nvars = parse(cnf_file, verbose=True)
    times = []
    start = time.time()
    dt_compiler = Dtree_Compiler(clausal_form.copy())
    dtree = dt_compiler.el2dt([2,3,4,1])
    dnnf_compiler = DNNF_Compiler(dtree)
    dnnf = dnnf_compiler.compile()
    times.append(time.time()-start)
    print('Exporting nnf file...')
    export_nnf_file(f'./demo_instances/{filename}/{encoding}_dnnf', dnnf)
    print('Exporting dtree dot file...')
    export_nnf_dot(f'./demo_instances/{filename}/{encoding}_dnnf')
    dnnf.reset()
    dnnf_smooth = copy.deepcopy(dnnf)
    print('Smoothing...')
    start = time.time()
    dnnf_smooth = dnnf_compiler.smooth(dnnf_smooth)
    times.append(time.time()-start)
    dnnf_smooth.reset()
    print('Exporting smooth nnf file...')
    export_nnf_file(f'./demo_instances/{filename}/{encoding}_sdnnf', dnnf_smooth)
    print('Exporting dot file...')
    export_nnf_dot(f'./demo_instances/{filename}/{encoding}_sdnnf')

    # Using separator as key
    print('================================================')
    print('Using separator as key')
    start = time.time()
    compiler = BDD_Compiler(nvars, clausal_form)
    obdd = compiler.compile(key_type='separator')
    times.append(time.time()-start)
    obdd.print_info(nvars)

    # # Using cutset as key
    # print('================================================')
    # print('Using cutset as key')
    # compiler = BDD_Compiler(nvars, clausal_form)
    # obdd = compiler.compile(key_type = 'cutset')
    # obdd.print_info(nvars)

    # Export dot file
    # export_nnf_file(f'./demo_instances/{filename}/obdd', obdd)
    export_dot_from_bdd(f'./demo_instances/{filename}/{encoding}_obdd.dot', obdd, nvars)
    print('End')
    return times

    
   

