#include <iostream>
#include <htslib/sam.h>

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <BAM file> <Chromosome> <Position>" << std::endl;
        return 1;
    }

    const char* bam_file = argv[1];
    const char* chromosome = argv[2];
    int position = std::stoi(argv[3]); // Convert position to integer

    // Open BAM file
    samFile* in = sam_open(bam_file, "r");
    if (!in) {
        std::cerr << "Error: Cannot open BAM file " << bam_file << std::endl;
        return 1;
    }

    // Load BAM header
    bam_hdr_t* header = sam_hdr_read(in);
    if (!header) {
        std::cerr << "Error: Cannot read BAM header." << std::endl;
        sam_close(in);
        return 1;
    }

    // Open index file
    hts_idx_t* idx = sam_index_load(in, bam_file);
    if (!idx) {
        std::cerr << "Error: BAM file must be indexed (.bai file required)." << std::endl;
        bam_hdr_destroy(header);
        sam_close(in);
        return 1;
    }

    // Get reference ID for the specified chromosome
    int ref_id = bam_name2id(header, chromosome);
    if (ref_id < 0) {
        std::cerr << "Error: Chromosome not found in BAM file." << std::endl;
        hts_idx_destroy(idx);
        bam_hdr_destroy(header);
        sam_close(in);
        return 1;
    }

    // Create iterator for the specified region
    hts_itr_t* iter = sam_itr_queryi(idx, ref_id, position - 1, position); // BAM is 0-based
    if (!iter) {
        std::cerr << "Error: Cannot create iterator for region." << std::endl;
        hts_idx_destroy(idx);
        bam_hdr_destroy(header);
        sam_close(in);
        return 1;
    }

    // Read alignments and count reads at the position
    bam1_t* read = bam_init1();
    int read_count = 0;
    while (sam_itr_next(in, iter, read) >= 0) {
        if (read->core.pos <= position - 1 && bam_endpos(read) >= position) {
            read_count++;
        }
    }

    // Output result
    std::cout << "Number of reads at " << chromosome << ":" << position << " = " << read_count << std::endl;

    // Cleanup
    bam_destroy1(read);
    hts_itr_destroy(iter);
    hts_idx_destroy(idx);
    bam_hdr_destroy(header);
    sam_close(in);

    return 0;
}

