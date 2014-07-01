from html.parser import HTMLParser


class Branch:
    '''part of a tree or something'''

    def __init__(self, tag, attrs, parent=None):
        self.parent = parent
        self.children = []

        self.tag = tag

        self.attrs = {}
        for k, v in attrs:
            entry = self.attrs.get(k, [])
            entry.append(v)
            self.attrs[k] = entry

        self._attrs = attrs

    def generator(self, onlybranches=True):
        # yield statement use ftw
        yield self
        for child in self.children:
            if type(child) == Branch:
                for result in child.generator(onlybranches):
                    yield result
            elif not onlybranches:
                yield child

    def close(self, tag):
        if tag != self.tag:
            raise Exception("</"+tag+"> closing but <"+self.tag+"> was opened")
        else:
            return self.parent

    def new(self, tag, attrs):
        child = Branch(tag, attrs, parent=self)
        self.children.append(child)
        return child

    def copy(self):
        c = Branch(self.tag, self._attrs, self.parent)
        for child in self.children:
            if type(child) == Branch:
                # recursive copy, setting up the family tree below me
                d = child.copy()
                d.parent = c
                c.children.append(d)
            else:
                c.children.append(child)
        return c

    def __str__(self):
        indent = " "*4
        attrs = ""
        for k, vs in self.attrs.items():
            for v in vs:
                # gesundheit!
                attrs += ' '+str(k)+'="'+str(v)+'"'
        sl = ['<'+self.tag+attrs+'>']
        for child in self.children:
            for line in str(child).splitlines():
                sl.append(indent+line)
        sl.append('</'+self.tag+'>')
        return '\n'.join(sl)

    def find_first(self, f=lambda x: True):
        # this will probably go away unless it's needed somewhere
        # find_all does everything and more, but also takes longer
        if not f(self):
            for child in self.children:
                if type(child) == Branch:
                    tmp = child.find(f)
                    if tmp:
                        return tmp
        else:
            return self

    def find_all(self, f=lambda x: True):
        results = []
        if f(self):
            results.append(self)
        # functional programming and recursion ftw
        [results.extend(y) for y in [child.find_all(f) for child in filter(lambda x: type(x) == Branch, self.children)]]
        return results

    def find_tag(self, tag):
        def helper(x):
            return x.tag == tag
        return self.find_all(helper)

    def find_attr(self, attrname, value=None):
        def helper(x):
            for k in x.attrs.get(attrname, []):
                if not value:
                    return True
                elif k == value:
                    return True
            return False
        return self.find_all(helper)

    def replacekids(self, newkids):
        self.children = newkids
        for kid in newkids:
            if type(kid) == Branch:
                kid.parent = self

    def clone(self):
        # create a twin of this subtree and place next to itself
        clone = self.copy()
        siblings = self.parent.children
        siblings.insert(siblings.index(self), clone)
        return clone

    def transplant(self, newbranches):
        siblings = self.parent.children
        # plants new branches in place of self
        try:
            i = siblings.index(self)
            # commit suicide
            siblings.pop(i)
        except ValueError:
            # parent didn't know of myself
            i = 0
        for newbranch in reversed(newbranches):
            if type(newbranch) == Branch:
                newbranch.parent = self.parent
            siblings.insert(i, newbranch)
        # shall we even return something?
        return newbranches
        # also, does python do reference counting? could we have a memleak?

        # raise Exception("call a lawyer, parent denies knowledge of child")

    def givekidstoparent(self):
        # have my parent adopt my children in my place, commit suicide
        siblings = self.parent.children
        for i in range(len(siblings)):
            candidate = siblings[i]
            if candidate == self:
                # commit suicide
                siblings.pop(i)
                # reverse the children list so we can do repeated correct insert
                for orphan in reversed(self.children):
                    if type(orphan) == Branch:
                        # make it official
                        orphan.parent = self.parent
                    # reversed iteration preserves order in this case
                    siblings.insert(i, orphan)


class NSFW(HTMLParser):

    def __init__(self, s=None):
        super().__init__()
        self.trees = []
        self.current = None
        if s:
            self.feed(s)

    def handle_starttag(self, tag, attrs):
        if self.current:
            self.current = self.current.new(tag, attrs)
        else:
            self.current = Branch(tag, attrs)
            self.trees.append(self.current)

    def handle_endtag(self, tag):
        # Branch.close returns parent. The parent of the root is "None"
        self.current = self.current.close(tag)

    def handle_data(self, data):
        data = data.strip()
        if data != '':
            if self.current:
                self.current.children.append(data)
            else:
                self.trees.append(data)
