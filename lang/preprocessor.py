class Preprocessor:
    def __init__(self, source: str):
        self.source = source
        self.preprocessed = []
        self.__preprocess()

    def __preprocess(self):
        line = 1
        for stream in self.source.split('\n'):
            clean_stream = ""
            stream = stream.strip().replace('\t', ' ')
            if stream.startswith("#"):
                line += 1
                continue

            if stream == "" or stream is None:
                line += 1
                continue

            # clean space and comment after a code
            space_seen = False
            for c in stream:
                if c == '#':
                    break
                if not c == chr(0x20) or not space_seen:
                    clean_stream += c
                    space_seen = False
                if c == chr(0x20):
                    space_seen = True

            self.preprocessed.append([clean_stream.strip(), line])
            line += 1

    def get_preprocessed(self) -> list:
        return self.preprocessed


