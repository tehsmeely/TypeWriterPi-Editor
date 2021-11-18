import toml

CONFIG_PATH = "config.toml"
EXPECTED_KEYS = [
    ["files"],
    ["files", "file_directory"],
    ["files", "temp_file_path"],
    ["theme"],
]


def _check_key(d, key):
    if len(key) == 0:
        return True
    else:
        try:
            this_key = key[0]
            val = d[this_key]
        except (TypeError, KeyError):
            return False
        else:
            return _check_key(val, key[1:])


def _assert_keys_present(d):
    keys_not_present = [key for key in EXPECTED_KEYS if not _check_key(d, key)]

    if len(keys_not_present) == 0:
        return
    else:
        raise Exception("Config is missing keys:", keys_not_present)


def load_config():
    with open(CONFIG_PATH) as f:
        conf = toml.load(f)
    _assert_keys_present(conf)
    return conf


if __name__ == "__main__":
    d = {"a": 2, "b": {"foo": "s"}}
    print(d)
    key = ["a"]
    print(key, _check_key(d, key))
    key = ["b"]
    print(key, _check_key(d, key))
    key = ["b", "foo"]
    print(key, _check_key(d, key))
    key = ["b", "bar"]
    print(key, _check_key(d, key))
    key = ["s"]
    print(key, _check_key(d, key))
