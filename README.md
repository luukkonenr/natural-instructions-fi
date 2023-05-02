# Finnish translations for [natural instructions v2](https://github.com/allenai/natural-instructions)

Known problems:
* non-categorical instance ids are off by +2


Original json-format is kept. Samples from a taskfile can be read for example like this:


```python
def parse_as_dict(path):
    with open(path) as fs:
        data = json.load(fs)
    instruction = data["Definition"]
    res = []
    for s in data["Instances"]:
        for response in s["output"]:
            sample =  {"instruction": data["Definition"], 
                "context": s["input"], 
                "response": response, 
                "id": s["id"]}
            yield sample

task = "translated_tasks/good_looking/categorical/fin-translated-task1289_trec_classification.json"
samples = parse_as_dict(task)
print(next(samples))

```
```bash
{'instruction': 'Sinulle annetaan kysymys. Sinun on määritettävä, mikä luokka kuvaa kysymystä paremmin. Kysymys kuuluu kuvausluokkaan, jos siinä kysytään kuvauksesta ja abstrakteista käsitteistä. Entiteettikysymykset koskevat entiteettejä, kuten eläimiä, värejä, urheilulajeja jne. Lyhennekysymykset kysyvät lyhenteistä ja lyhennetyistä ilmauksista. Ihmisiä, henkilön kuvausta ja henkilöiden ryhmää tai organisaatiota koskevat kysymykset luokitellaan luokkaan Ihminen. Määräkysymykset koskevat numeerisia arvoja ja sijaintikysymykset sijainteja, kaupunkeja ja maita. Vastaus saa olla pituudeltaan yhden sanan. Vastaa "Kuvaus", "Entiteetti", "Lyhenne", "Henkilö", "Määrä" tai "Sijainti".',
 'context': 'Kuka omistaa televisio-ohjelman oikeudet ?',
 'response': 'Henkilö',
 'id': 'task1289-aaf4993ab782493e89f1b90b3a257f0c'}
 ```
