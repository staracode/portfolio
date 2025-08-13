#!/usr/bin/env nextflow
/*
============================================================
 Groovy Syntax Cheatsheet for Nextflow
 Author: Tara Friedrich
 Purpose: Quick reference of Groovy basics used in Nextflow
============================================================
*/

// ---------------------------------------------------------
// 1. VARIABLES
// ---------------------------------------------------------
x = 42                     // Dynamic type
int y = 10                 // Explicit type
String name = 'Nextflow'   // String variable
final PI = 3.1415          // Constant

println "Variables: x=$x, y=$y, name=$name, PI=$PI"

// ---------------------------------------------------------
// 2. STRINGS
// ---------------------------------------------------------
sample_id = "sample_${x}"  // Interpolation
multi_line = """This
is
multiline."""
println sample_id
println multi_line

// ---------------------------------------------------------
// 3. LISTS & MAPS
// ---------------------------------------------------------
myList = [1, 2, 3, 4]
println myList[0]      // First element
println myList[-1]     // Last element

myMap = [id: 'sample1', type: 'RNA']
println myMap.id
println myMap['type']

// ---------------------------------------------------------
// 4. CLOSURES (Anonymous Functions)
// ---------------------------------------------------------
square = { num -> num * num }
println square(4)   // 16

[1, 2, 3].each { println it } // Implicit "it"

// -------------------------------------------------

