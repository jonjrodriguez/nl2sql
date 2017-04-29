from nltk.parse.stanford import StanfordParser

class MyParser(StanfordParser):
    def raw_parse_sents(self, sentences, verbose=False):
        cmd = [
            self._MAIN_CLASS,
            '-model', self.model_path,
            '-sentences', 'newline',
            '-outputFormat', 'wordsAndTags,penn,typedDependencies',
        ]

        print self._execute(cmd, '\n'.join(sentences), verbose)
