import hashlib
import warnings
import subprocess
from typing import List, Optional, Dict, Any


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

# taken from pydantic
# https://github.com/pydantic/pydantic/blob/fd2991fe6a73819b48c906e3c3274e8e47d0f761/pydantic/utils.py#L200
#
# The MIT License (MIT)
#
# Copyright (c) 2017 - 2022 Samuel Colvin and other contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def deep_update(
    mapping: Dict[Any, Any], *updating_mappings: Dict[Any, Any]
) -> Dict[Any, Any]:
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in updated_mapping \
                    and isinstance(updated_mapping[k], dict) \
                    and isinstance(v, dict):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping
