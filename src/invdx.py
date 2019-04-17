# invdx.py
# An inverted index
__author__ = 'Nick Hirakawa'


class InvertedIndex:

    def __init__(self):
        self.index = dict()

    def __contains__(self, item):
        return item in self.index

    def __getitem__(self, item):
        return self.index[item]

    def add(self, word, doc_id):
        if word in self.index:
            if doc_id in self.index[word]:
                self.index[word][doc_id] += 1
            else:
                self.index[word][doc_id] = 1
        else:
            d = dict()
            d[doc_id] = 1
            self.index[word] = d

    # frequency of word in document
    def get_document_frequency(self, word, docid):
        if word in self.index:
            if docid in self.index[word]:
                return self.index[word][docid]
            else:
                raise LookupError('%s not in document %s' % (str(word), str(docid)))
        else:
            raise LookupError('%s not in index' % str(word))

    # frequency of word in index, i.e. number of documents that contain word
    def get_index_frequency(self, word):
        if word in self.index:
            return len(self.index[word])
        else:
            raise LookupError('%s not in index' % word)


class DocumentLengthTable:

    def __init__(self):
        self.table = dict()

    def __len__(self):
        return len(self.table)

    def add(self, doc_id, length):
        self.table[doc_id] = length

    def get_length(self, doc_id):
        if doc_id in self.table:
            return self.table[doc_id]
        else:
            raise LookupError('%s not found in table' % str(doc_id))

    def get_average_length(self):
        sum = 0
        for length in self.table.items():
            sum += length[1]
        return float(sum) / float(len(self.table))


def build_data_structures(corpus):
    idx = InvertedIndex()
    dlt = DocumentLengthTable()
    for doc_id in corpus:

        # build inverted index
        for word in corpus[doc_id]:
            idx.add(str(word), str(doc_id))

        # build document length table
        length = len(corpus[str(doc_id)])
        dlt.add(doc_id, length)

    return idx, dlt
