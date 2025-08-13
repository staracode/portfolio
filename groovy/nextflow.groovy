#!/usr/bin/env nextflow
/*
 * nextflow_upper_triangle_compare.nf
 * Compare files pairwise in upper triangle fashion inside Nextflow
 */

params.files = file(params.files ?: '*.txt')  // pass files via --files or match pattern

// Create a list of files
file_list = params.files.collect { it.toString() }

// Create a channel of upper triangle file pairs
pairs_ch = Channel
    .from(file_list)
    .flatMap { f1 ->
        file_list.findAll { f2 -> file_list.indexOf(f2) > file_list.indexOf(f1) }
                .collect { f2 -> [file(f1), file(f2)] }
    }

// Process to compare file contents
process COMPARE {
    input:
    tuple val(f1), val(f2)

    output:
    stdout into results_ch

    script:
    """
    if diff -q ${f1} ${f2} > /dev/null; then
        echo "${f1} vs ${f2}: SAME"
    else
        echo "${f1} vs ${f2}: DIFFERENT"
    fi
    """
}

// Print results
results_ch.view()

