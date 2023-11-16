from NetworkGenerators.generators import *
from EncodingCompilers.encodings import *
from KnowledgeCompilers.main import *
import time

if __name__ == "__main__":
    demo_name = "alarm"
    model = None
    #switch case on demo
    if demo_name == "asia":
        model = generate_asia_model()
    elif demo_name == "alarm":
        model = generate_alarm_model()
    elif demo_name == "cancer":
        model = generate_cancer_model()
    else:
        print("Invalid demo")
        exit()
    # generate ENC1 encoding
    print("Generating ENC1 encoding...")
    start= time.time() #start timer
    encoding_ENC1_raw, encoding_ENC1_dimacs = generate_ENC1_encoding(model)
    enc1_time = [time.time()-start,0,0,0] #end timer
    #save the raw encoding to file (for debugging)
    with open(f"./demo_instances/{demo_name}/enc1_raw.cnf", "w", encoding="utf-8") as f:
        f.write(str(encoding_ENC1_raw))
    #save the dimacs encoding to file (for running)
    with open(f"./demo_instances/{demo_name}/enc1_dimacs.cnf", "w") as f:
        f.write(str(encoding_ENC1_dimacs))
    enc1_time[1:] = generate_theory_from_cnf(demo_name,encoding='enc1')

    #generate ENC2 encoding
    print("Generating ENC2 encoding...")
    start= time.time() #start timer
    encoding_ENC2_raw, encoding_ENC2_dimacs = generate_ENC2_encoding(model)
    enc2_time = [time.time()-start,0,0,0] #end timer
    #save the raw encoding to file (for debugging)
    with open(f"./demo_instances/{demo_name}/enc2_raw.cnf", "w", encoding="utf-8") as f:
        f.write(str(encoding_ENC2_raw))
    #save the dimacs encoding to file (for running)
    with open(f"./demo_instances/{demo_name}/enc2_dimacs.cnf", "w") as f:
        f.write(str(encoding_ENC2_dimacs))
    enc2_time[1:] = generate_theory_from_cnf(demo_name,encoding='enc2')

    print("Displaying compilation times")
    print("Schema|Encoding Generation|DNNF|Smooth DNNF|OBDD|")
    print("ENC1|" + str(enc1_time[0]) + "|" + str(enc1_time[1]) + "|" + str(enc1_time[2]) + "|" + str(enc1_time[3]) + "|")
    print("ENC2|" + str(enc2_time[0]) + "|" + str(enc2_time[1]) + "|" + str(enc2_time[2]) + "|" + str(enc2_time[3]) + "|")

# to get the number of edges and nodes in the dot files, run the following commands:
# (Note that for dnnf and sdnnf, this info is also present in the raw files)
# gc -n -e sample.dot
    
# to generate the pngs and svgs from the dot files, run the following commands:
# dot -Tpng enc1_dnnf.dot -o enc1_dnnf.png
# dot -Tsvg enc1_dnnf.dot -o enc1_dnnf.svg
# dot -Tpng enc1_sdnnf.dot -o enc1_sdnnf.png
# dot -Tsvg enc1_sdnnf.dot -o enc1_sdnnf.svg
# dot -Tpng enc1_obdd.dot -o enc1_obdd.png
# dot -Tsvg enc1_obdd.dot -o enc1_obdd.svg
# dot -Tpng enc2_dnnf.dot -o enc2dnnf.png
# dot -Tsvg enc2_dnnf.dot -o enc2dnnf.svg
# dot -Tpng enc2_sdnnf.dot -o enc2_sdnnf.png
# dot -Tsvg enc2_sdnnf.dot -o enc2_sdnnf.svg
# dot -Tpng enc2_obdd.dot -o enc2obdd.png
# dot -Tsvg enc2_obdd.dot -o enc2obdd.svg