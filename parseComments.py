import zstandard as zstd
import sys
import simplejson as json

file = "RC_2019-12.zst"

with open(file, 'rb') as fh:
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(fh) as reader:
        previous_line = ""
        while True:
            chunk = reader.read(65536)
            if not chunk:
                break

            string_data = chunk.decode('utf-8')
            lines = string_data.split("\n")
            for i, line in enumerate(lines[:-1]):
                if i == 0:
                    line = previous_line + line
                object = json.loads(line)
                print(object)
                sys.exit()
                # do something with the object here
            previous_line = lines[-1]
