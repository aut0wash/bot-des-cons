import json
import logging


class AudioSample:
    def __init__(self, name, path, tags, users, volume, num_played):
        self.name = name
        self.path = path
        self.tags = tags
        self.users = users
        self.volume = volume
        self.num_played = num_played

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["path"], data["tags"], data["users"], data["volume"], data["num_played"])

    def print(self):
        logging.info(f"Name: {self.name}, path: {self.path}, tags: {self.tags}, users: {self.users}, volume: {self.volume}, played: {self.num_played}")


def load_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data


def get_sample_from_id(samples, sample_id):
    try:
        return AudioSample.from_dict(samples[str(sample_id)])
    except Exception as e:
        logging.error('Error in get_sample_from_id: {}'.format(e))
        return None


def get_sample_from_name(samples, sample_name):
    try:
        for sample in samples:
            if samples[sample]["name"] == sample_name:
                return AudioSample.from_dict(samples[sample])
    except Exception as e:
        logging.error('Error in get_sample_from_name: {}'.format(e))
        return None


if __name__ == "__main__":
    samples = load_json("samples.json")
    sample = get_sample_from_id(samples, 1)
    sample.print()
    sample = get_sample_from_name(samples, "invoker")
    sample.print()
