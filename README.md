# Finnish translations for [natural instructions v2](https://github.com/allenai/natural-instructions)

## Process
1) run `python scripts/json2doc.py <FILES> --prefix <PREFIX>` or `run python scripts/categorical_json2doc.py <FILES> --prefix <PREFIX>`, depending whether to have outputs for each sample alongside during the translation process or translate outputs only once. (categorical) 
2) Run generated docx-files through DeepL
3) run `python scripts/doc2json.py <FILES> --meta_data <PATH_TO_METADATA_FILE>` or `python scripts/doc2json.py <FILES> --meta_data <PATH_TO_METADATA_FILE>` to produce json-files under the `doc_out/fin-translated-<task-name-in-metadata-file>`
4) Manually fix files
5) Add alternative phrasings to "Definition" to enrichen prompts.




Original json-format is kept. Samples from a taskfile can be read for example like this:


```python
import random
def parse_as_dict(path):
    with open(path) as fs:
        data = json.load(fs)
    res = []
    for s in data["Instances"]:
        for response in s["output"]:
            prompt_idx = random.randint(0,len(data["Definition"])-1)
            sample =  {"instruction": data["Definition"][prompt_idx], 
                "context": s["input"], 
                "response": response, 
                "id": s["id"]}
            yield sample

task = "translated_tasks/good_looking/categorical/fin-translated-task1289_trec_classification.json"
sample_generator = parse_as_dict(task)
print(next(sample_generator))
```
```bash
{'instruction': 'Sinulle annetaan kysymys. Sinun on määritettävä, mikä luokka kuvaa kysymystä paremmin. Kysymys kuuluu kuvausluokkaan, jos siinä kysytään kuvauksesta ja abstrakteista käsitteistä. Entiteettikysymykset koskevat entiteettejä, kuten eläimiä, värejä, urheilulajeja jne. Lyhennekysymykset kysyvät lyhenteistä ja lyhennetyistä ilmauksista. Ihmisiä, henkilön kuvausta ja henkilöiden ryhmää tai organisaatiota koskevat kysymykset luokitellaan luokkaan Ihminen. Määräkysymykset koskevat numeerisia arvoja ja sijaintikysymykset sijainteja, kaupunkeja ja maita. Vastaus saa olla pituudeltaan yhden sanan. Vastaa "Kuvaus", "Entiteetti", "Lyhenne", "Henkilö", "Määrä" tai "Sijainti".',
 'context': 'Kuka omistaa televisio-ohjelman oikeudet ?',
 'response': 'Henkilö',
 'id': 'task1289-aaf4993ab782493e89f1b90b3a257f0c'}
 ```
