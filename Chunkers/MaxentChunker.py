import nltk

class ConsecutiveNPChunkTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (_, tag) in enumerate(tagged_sent):
                feature_set = npchunk_features(untagged_sent, i, history)
                train_set.append((feature_set, tag))
                history.append(tag)

        self.classifier = nltk.MaxentClassifier.train(train_set)

    def tag(self, sentence):
        history = []
        for i, _ in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)

        return zip(sentence, history)

class MaxentChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        tagged_sents = [[((word, tag), chunk) for (word, tag, chunk)
                         in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]

        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conll_tags = [(word, tag, chunk) for ((word, tag), chunk) in tagged_sents]

        return nltk.chunk.util.conlltags2tree(conll_tags)

def npchunk_features(sentence, i, history):
    word, pos = sentence[i]

    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]

    if i == len(sentence)-1:
        nextword, nextpos = "<END>", "<END>"
    else:
        nextword, nextpos = sentence[i+1]

    return {
        "pos": pos,
        "word": word,
        "prevpos": prevpos,
        "nextpos": nextpos,
        "prevpos+pos": "%s+%s" % (prevpos, pos),
        "pos+nextpos": "%s+%s" % (pos, nextpos),
        "tags-since-dt": tags_since_dt(sentence, i)
    }

def tags_since_dt(sentence, i):
    tags = set()

    for word, pos in sentence[:i]:
        if pos == 'DT':
            tags = set()
        else:
            tags.add(pos)

    return '+'.join(sorted(tags))
