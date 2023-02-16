import hashlib
import warnings
import subprocess
from typing import List, Optional


def get_file_hash(fname, chunksize=128*1024, algo='blake2b'):
    # based on a post by quantumSoup (https://stackoverflow.com/a/3431838)
    # CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/
    if algo == 'blake2b':
        hash_func = hashlib.blake2b()
    elif algo == 'md5':
        # deprecated, but available for backward compatibility
        msg = [
            "MD5 checksum is deprecated.",
            "Consider using \'blake2b\' or \'sha3\'"
        ]
        warnings.warn(" ".join(msg), DeprecationWarning)
        hash_func = hashlib.md5()
    elif algo == 'sha3':
        hash_func = hashlib.sha3_512()
    else:
        msg = [
            f"The supplied hash-algorithm {algo} is not supported.",
            "Consider using \'blake2b\' or \'sha3\'."
        ]
        raise ValueError(" ".join(msg))

    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(chunksize), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def get_git_revision_hash() -> str:
    # Copyright 2014 Yuji 'Tomita' Tomita
    # (https://stackoverflow.com/a/21901260)
    # CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/
    cmd = ['git', 'rev-parse', 'HEAD']
    return subprocess.check_output(cmd).decode('ascii').strip()


def split_string_to_size(
    string: str,
    max_len: int,
    sep: Optional[str] = None,
) -> List[str]:
    if (size := len(string)) <= max_len:
        return [string]
    if sep is None:
        mod = size // max_len
        counts = mod if size % max_len == 0 else mod+1
        return [
            string[i*max_len:(i+1)*max_len] for i in range(counts)
        ]
    else:
        parts = string.split(sep)
        result = []
        current = []
        cum_size = 0
        for part in parts:
            cum_size += len(part)
            if cum_size > max_len:
                if current:
                    result.append(sep.join(current))
                current = [part]
                cum_size = len(part) + 1
            else:
                current.append(part)
                cum_size += 1
        if current:
            result.append(sep.join(current))
        return result
