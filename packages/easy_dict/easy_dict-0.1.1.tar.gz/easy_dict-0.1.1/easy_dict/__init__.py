"""The MIT License (MIT)
Copyright (c) 2016 Cahyo Primawidodo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

__author__ = 'cahyo primawidodo'
__version__ = '0.1.1'


from collections.abc import MutableMapping


class NestedDict(MutableMapping):

    def __init__(self, initial_value=None, root=True):
        super().__init__()
        self._val = {}
        if initial_value is not None:
            self._val.update(initial_value)
        self._found = False
        self._root = root

    def __getitem__(self, item):
        self._found = False

        def _look_deeper():
            result = tuple()
            for k, v in self._val.items():
                if isinstance(v, dict):
                    n = NestedDict(self[k], root=False)
                    if n[item]:
                        result += (n[item],)
                    self._found = self._found or n._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    # result = self[item] = type(self)()
                    raise KeyError(item)

            result = result[0] if len(result) == 1 else result

            return result

        def _process_list():
            if len(item) == 1:
                return self[item[0]]
            trunk, *branches = item
            nd = NestedDict(self[trunk], root=False)
            return nd[branches] if len(branches) > 1 else nd[branches[0]]

        if isinstance(item, list):
            return _process_list()

        elif self.__isstring_containing_char(item, '/'):
            item = item.split('/')
            return _process_list()

        elif item in self._val:
            # TODO getting multiple keys failed when there's one at root. should look deeper first.
            self._found = True
            return self._val.__getitem__(item)

        else:
            return _look_deeper()

    def __setitem__(self, branch_key, value):
        self._found = False

        def _process_list():
            *branches, tip = branch_key

            if self[tip]:
                if isinstance(self[tip], tuple):
                    if isinstance(self[branches], tuple):
                        raise KeyError('ambiguous keys={!r}'.format(branch_key))
                    else:
                        self[branches][tip] = value
                else:
                    self[tip] = value
            else:
                raise KeyError('no key found={!r}'.format(tip))

        def _look_deeper():
            nd = NestedDict(root=False)
            for k, v in self._val.items():
                if v and (isinstance(v, dict) or isinstance(v, NestedDict)):
                    nd._val = self._val[k]
                    nd[branch_key] = value
                    self._found = self._found or nd._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    self._val.__setitem__(branch_key, value)

        if isinstance(branch_key, list) or isinstance(branch_key, tuple):
            _process_list()

        elif self.__isstring_containing_char(branch_key, '/'):
            branch_key = branch_key.split('/')
            _process_list()

        elif branch_key in self._val:
            self._found = True
            self._val.__setitem__(branch_key, value)

        else:
            _look_deeper()

    def __delitem__(self, key):
        self._val.__delitem__(key)

    def __iter__(self):
        return self._val.__iter__()

    def __len__(self):
        return self._val.__len__()

    def __repr__(self):
        return __name__ + str(self._val)

    def __call__(self):
        return self._val

    def __contains__(self, item):
        return self._val.__contains__(item)

    def anchor(self, trunk, branch, value=None):
        nd = NestedDict(root=False)
        for k, v in self._val.items():
            if v and isinstance(v, dict):
                nd._val = self._val[k]
                nd.anchor(trunk, branch, value)
                self._found = self._found or nd._found

            if k == trunk:
                self._found = True
                if not isinstance(self._val[trunk], dict):
                    if self._val[trunk]:
                        raise ValueError('value of this key is not a logical False')
                    else:
                        self._val[trunk] = {}  # replace None, [], 0 and False to {}
                self._val[trunk][branch] = value

        if self._root:
            if self._found:
                self._found = False
            else:
                raise KeyError

    def setdefault(self, key, default=None):

        if isinstance(key, list) or isinstance(key, tuple):
            # TODO tests this
            trunk, *branches = key

            self._val.setdefault(trunk, {})
            if self._val[trunk]:
                pass
            else:
                self._val[trunk] = default

            nd = NestedDict(self[trunk], root=False)
            if len(branches) > 1:
                nd[branches] = default
            elif len(branches) == 1:
                nd._val[branches[0]] = default
            else:
                raise KeyError
        else:
            self._val.setdefault(key, default)


    @staticmethod
    def __isstring_containing_char(obj, char):
        if isinstance(obj, str):
            if char in obj:
                return True
        return False


def asciify(d: dict, is_root=True, al=list, lvl=0):
    if is_root:
        al = []
        lvl = 0

    if d:
        for k, v in d.items():
            il = []
            for i in range(lvl):
                if i == lvl - 1:
                    il.append('`-- ')
                else:
                    il.append('    ')
            il.append(k)
            al.append(il)

            if d[k]:
                lvl += 1
                al = asciify(d[k], is_root=False, al=al, lvl=lvl)
                lvl -= 1

    if is_root:
        empt_fill = '    '
        vert_fill = '|   '
        end__fill = '`-- '
        plus_fill = '+-- '

        replacement = set()
        for each_line in reversed(al):

            to_remove = []
            for index in replacement:
                if each_line[index] == empt_fill:
                    each_line[index] = vert_fill
                elif each_line[index] == end__fill:
                    each_line[index] = plus_fill
                else:
                    to_remove.append(index)

            while to_remove:
                replacement.discard(to_remove.pop())

            for i, e in enumerate(each_line):
                if e == end__fill:
                    replacement.add(i)

        sl = [''.join(x) for x in al]

        return sl
    else:
        return al
