import json
import os
import re


dir_path = os.path.dirname(os.path.realpath(__file__))


def get_data(
    path: str
    ) -> list:
    data = []
    for f in os.listdir(path):
        # print(f"processing {f}")
        if f.startswith("watch-history") and f.endswith(".json"):
            with open(f"{path}/{f}", 'r') as fi:
                d = json.load(fi)
                for line in d:
                    data.append(line)
    return data


def make_count(
        data: list,
    ) -> dict:
    aggr = {
        "seen": 0,
        "title_words": {
        },
        "user_names": {},
    }
    for d in data:
        title = d.get("title", "")
        # scrub away all the characters we dont care about
        scrubbed = re.sub(r'[^ \w+]', '', title)
        for w in scrubbed.split()[1:]:
            # lets get rid of all them capitals, silly things
            word = w.lower()
            if len(word) <= 3:
                continue
            if word in aggr["title_words"]:
                aggr["title_words"][word] += 1
            else:
                aggr["title_words"][word] = 1
        subtitles = d.get("subtitles", [])
        for n in subtitles:
            name = n.get("name", "")
            if name in aggr["user_names"]:
                aggr["user_names"][name] += 1
            else:
                aggr["user_names"][name] = 1
        aggr["seen"] += 1
    return aggr


def sort_output(processed):
    result = {}
    for k, v in processed.items():
        if isinstance(v, dict):
            result[k] = {k: v for k, v in sorted(v.items(), key=lambda item: item[1], reverse=True)}
            continue
        result[k] = v
    return result


if __name__ == "__main__":
    # print("processing data...")
    raw_data = get_data(dir_path+"/data")
    processed = make_count(raw_data)

    pr_clean = sort_output(processed)

    print(json.dumps(pr_clean))
