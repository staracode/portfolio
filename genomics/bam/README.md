
# BAM File Processing with htslib

This project uses the `htslib` library to manipulate and process BAM files, enabling the extraction of information about reads at specific genomic locations.

## Installation

To get started, you'll need to install `htslib` via Homebrew:

```bash
brew install htslib
brew --prefix htslib
```

Run the tool
```bash
g++ -o bam bam.cpp -I/opt/homebrew/Cellar/htslib/1.21/include -L/opt/homebrew/Cellar/htslib/1.21/lib -lhts
./bam example/small.bam X 1017741
```

Number of reads at X:1017741 = 19
