# Gakp-pyfunk
A set of functional tools for python. It is supposed to have the same interface as Gakp-jsfunk and Gakp-lispfunk

## Example
```python
from pyfunk.combinators import compose
from pyfunk.collections import fmap
from pyfunk.functors.io import IO


def get_file(filename):
    '''@sig get_file :: String -> IO String '''
    def open_file():
        with open(filename) as f:
            return f.read()
    return IO(open_file)


def get_tokens(str):
    return str.split()


def get_lenght_of_tokens(tokens):
    return len(tokens)

tokenLength = compose(fmap(get_lenght_of_tokens), fmap(get_tokens), get_file)
print(tokenLength('.gitignore').unsafeIO())
```

## Contributing
Anyone can contribute using the fork and pull model.

