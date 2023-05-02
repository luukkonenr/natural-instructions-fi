# Finnish translations for natural instruction v2

Known problems:
* non-categorical instance ids are off by +2

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
                "response": s["output"], 
                "id": s["id"]}
            yield sample

task = "translated_tasks/good_looking/categorical/fin-translated-task1289_trec_classification.json"
samples = parse_as_dict(task)
next(samples)

```
