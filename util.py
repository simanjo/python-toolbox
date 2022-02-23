#%%
import hashlib
import warnings

def get_file_hash(fname, chunksize=4096, algo='blake2b'):
    # based on a post by quantumSoup (https://stackoverflow.com/a/3431838)
    # CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/
    if algo == 'blake2b':
        hash_func = hashlib.blake2b()
    elif algo == 'md5':
        # deprecated, but available for backward compatibility
        msg = f"MD5 checksum is deprecated. Consider using \'blake2b\' or \'sha3\'"
        warnings.warn(msg, DeprecationWarning)
        hash_func = hashlib.md5()
    elif algo == 'sha3':
        hash_func = hashlib.sha3_512()
    else:
        msg = f"The supplied hash-algorithm {algo} is not supported. " \
            + "Consider using \'blake2b\' or \'sha3\'."
        raise(ValueError(msg))

    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(chunksize), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()
