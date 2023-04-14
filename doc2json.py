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
    doc_sep = "task"        # field "Definition" in the original document
    inst_sep = "example"    # field "Instances" in orig doc
    output_sep = "result"   # newline-separated list in the output string

    is_task_sep = lambda p: p.runs[0].bold and p.runs[0].underline and p.text.lower().startswith(doc_sep)
    is_instance_sep = lambda p: p.runs[0].bold and p.text.lower().startswith(inst_sep)
    is_output_sep = lambda p: p.runs[0].bold and p.text.lower().startswith(output_sep)

    meta = json.load(open(args.meta_data))
    meta_idx = 0
    # paths = sorted(glob.glob("doc_in/*docx"))
    pgraph_iter = paragraph_generator(args.DOCX)
    for p in pgraph_iter:
        if is_task_sep(p):
            if curr_doc.get("Definition"):
                curr_doc.update({"Instances": instances})
                instances = list()
                curr_instance = dict()
                combine_original_meta(meta[meta_idx]['file'], curr_doc)
                task_docs.append(curr_doc)
                write_output_file(meta[meta_idx]["file"], curr_doc)

                print("Finished one task", p.text)
                curr_doc = dict()

            p = next(pgraph_iter)
            curr_doc.update({"Definition": [p.text]}) 
        
        elif is_instance_sep(p):
            if curr_instance.get("input"):
                instances.append(curr_instance)
                meta_idx+=1
                curr_instance = dict()

            p = next(pgraph_iter)
            curr_instance.update({"input": p.text})
            curr_instance.update({"id": meta[meta_idx]["uuid"]})

        elif is_output_sep(p):
            p = next(pgraph_iter)
            curr_instance.setdefault("output", []).append(p.text)

    # Append the last sample
    instances.append(curr_instance)
    curr_doc.update({"Instances": instances})
    combine_original_meta(meta[meta_idx]['file'], curr_doc)
    task_docs.append(curr_doc)
    write_output_file(meta[meta_idx]['file'], curr_doc)