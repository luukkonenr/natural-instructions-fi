
import json
import glob 
import os
import docx
import tqdm 
import argparse

# Yield only if task is monolingual

def yield_docs(paths):
    for path in sorted(paths):
        with open(path) as f:
            doc = json.load(f)

        if  doc["Input_language"][0] == doc["Output_language"][0] == doc["Instruction_language"][0] == "English":
            yield (doc, path)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta_data", help="Json with metadata created by doc2json")
    ap.add_argument("DOCX", nargs="+", help="All translated docs in their correct order")
    args = ap.parse_args()
    # paths = sorted(glob.glob("../natural-instructions/tasks/task00[0-5]*json"))

    doclist = list()
    doc_counter=0
    doc=docx.Document()
    current_len=0
    max_len=950_000

    for d_idx, (d, doc_name) in enumerate(yield_docs(args.DOCXS)):
        instances, definition = [d.pop(key) for key in ["Instances", "Definition"]]

        pgraph=doc.add_paragraph("")
        r = pgraph.add_run(f"Task number {d_idx}") # Definition -> task
        r.bold=True
        r.underline=True
        doc.add_paragraph(definition)    
        for sample_idx, sample in tqdm.tqdm(enumerate(instances)):

            sample_len = sum([len(sample[k]) for k in ["input", "output"]])

            # print(current_len + sample_len)
            if (current_len + sample_len) > max_len:
                #Save first!
                doc.save(f"doc_in/natural_inst-{doc_counter:05d}.docx")
                doc_counter+=1
                current_len=0
                doc=docx.Document()

            doclist.append(
                {"file": doc_name, 
                "idx": sample_idx, 
                "outputs": len(sample["output"]), 
                "uuid": sample["id"], 
                })

            pgraph=doc.add_paragraph("")
            r=pgraph.add_run(f"Example {d_idx}.{sample_idx}") # adds to the previous paragraph
            r.bold=True
            pgraph=doc.add_paragraph(fr'{sample["input"]}')

            for out_idx, entry in enumerate(sample["output"]):
                pgraph=doc.add_paragraph("")
                r = pgraph.add_run(f"Result") # output -> result
                r.bold=True
                doc.add_paragraph(entry)       
    
            current_len+=sample_len    

        doc.save(f"doc_in/natural_inst-{doc_counter:05d}.docx")
        # doc_counter+=1


    with open("doc_in/metadata.json","wt") as f:
        json.dump(doclist,f)