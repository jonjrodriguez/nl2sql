import nltk

class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(tag, chunk) for _, tag, chunk in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]

        self.tagger = nltk.UnigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunk_tags = [chunk_tag for (pos, chunk_tag) in tagged_pos_tags]
        conll_tags = [(word, pos, chunktag) for ((word, pos), chunktag)
                      in zip(sentence, chunk_tags)]

        return nltk.chunk.util.conlltags2tree(conll_tags)
