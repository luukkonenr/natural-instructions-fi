import json
import glob 
import os
import docx
import tqdm 
import argparse

def paragraph_generator(paths):
    for path in paths:
        d = docx.Document(path)
        for p in d.paragraphs:
            yield p

def combine_original_meta(orig_path, res_doc):
    f = json.load(open(orig_path))
    _ = [f.pop(key) for key in ["Instances", "Definition"]]
    res_doc.update(f)
    return res_doc

def write_output_file(meta_path, doc):
    out_path = "doc_out/fin-translated-" + os.path.basename(meta_path)
    with open(out_path, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print(out_path)

def yield_category_map(meta_path, new_levels, task_idx):
    meta_categs = json.load(open(args.meta_data.split(".")[0]+"_category_map.json"))


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("--meta_data", help="Json with metadata created by doc2json")
    ap.add_argument("DOCX", nargs="+", help="All translated docs in their correct order")
    args = ap.parse_args()

    task_docs = list()
    instances = list()
    curr_doc = dict()
    curr_instance = dict()

    # Change these after translation
    doc_sep = "Tehtävän numero".lower()
    inst_sep = "Esimerkki".lower()
    level_sep = "Taso".lower()
    # doc_sep = "Tehtävän numero".lower()        # field "Definition" in the original document
    # inst_sep = "Esimerkki".lower()    # field "Instances" in orig doc
    # output_sep = "Tulos".lower()   # newline-separated list in the output string

    is_task_sep = lambda p: p.runs[0].bold and p.runs[0].underline
    is_instance_sep = lambda p: p.runs[0].bold and p.text.lower().startswith(inst_sep)
    is_level_sep = lambda p: p.runs[0].underline and p.text.lower().startswith(level_sep)

    meta = json.load(open(args.meta_data))
    meta_idx = 0
    
    meta_categs = json.load(open(args.meta_data.split(".")[0]+"_category_map.json"))
    # paths = sorted(glob.glob("doc_in/*docx"))
    pgraph_iter = paragraph_generator(args.DOCX)
    
    prev_header = ""
    categ_mapper = {}
    levels = list()
    for p in pgraph_iter:
        # print(meta_idx, end="\r")
        if is_task_sep(p):

            prev_header = p.text
            if curr_doc.get("Definition"):
                instances.append(curr_instance)
                curr_doc.update({"Instances": instances})
                # Write task<>.json-file at each instance header
                combine_original_meta(meta[meta_idx]['file'], curr_doc)
                task_docs.append(curr_doc)
                write_output_file(meta[meta_idx]["file"], curr_doc)

                print()
                print("Finished one task, moving to:", p.text)
                instances = list()
                curr_instance = dict()
                curr_doc = dict()
                levels = list()
                categ_mapper = {}
                meta_idx+=1 

            p = next(pgraph_iter)
            curr_doc.update({"Definition": [p.text]}) 

        elif is_level_sep(p):
            prev_header = p.text
            p = next(pgraph_iter)
            levels.append(p.text)

        elif is_instance_sep(p):
            # print(p.text)
            print(prev_header)
            print(p.text)
            if prev_header.lower() == level_sep:
                f = meta[meta_idx]["file"]
                orig_categs = meta_categs[f]
                categ_mapper = {k:v for (k, v) in zip(orig_categs, levels)}


            prev_header = p.text
            
            if curr_instance.get("input"):
                instances.append(curr_instance)
                meta_idx+=1 # need to increase meta-file indexing
                curr_instance = dict()


            p = next(pgraph_iter)
            curr_instance.update({"input": p.text})
            curr_instance.update({"id": meta[meta_idx]["uuid"]})

            print(categ_mapper)
            # map translated keys here
            orig_outputs = meta[meta_idx]["outputs"]
            trans_outputs = [categ_mapper[output] for output in orig_outputs]
            curr_instance.update({"output": trans_outputs})

    print(curr_instance)
    # Append the last sample
    instances.append(curr_instance)
    curr_doc.update({"Instances": instances})
    combine_original_meta(meta[meta_idx]['file'], curr_doc)
    task_docs.append(curr_doc)
    write_output_file(meta[meta_idx]['file'], curr_doc)

    print("Finished succesfully")