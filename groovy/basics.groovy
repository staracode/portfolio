#!/usr/bin/env groovy

println "\n=== 1. Basic closure ==="
def sayHello = { println "Hello from a closure!" }
sayHello()

println "\n=== 2. Closure with parameters ==="
def greet = { String name -> println "Hello, $name!" }
greet("Tara")

println "\n=== 3. Implicit 'it' parameter ==="
def printDouble = { println it * 2 }
printDouble(5)  // 'it' = 5

println "\n=== 4. Closures with collections ==="
def nums = [1, 2, 3, 4, 5]
println "Each:"
nums.each { println "Number: $it" }

println "Collect (squares): ${nums.collect { it * it }}"
println "Find first > 3: ${nums.find { it > 3 }}"
println "Find all even: ${nums.findAll { it % 2 == 0 }}"
println "Sum using inject: ${nums.inject(0) { sum, val -> sum + val }}"

println "\n=== 5. Closures capturing outer variables ==="
def factor = 3
def multiply = { n -> n * factor }  // factor is from outer scope
println "5 * factor = ${multiply(5)}"

println "\n=== 6. Passing closures to functions ==="
def applyTwice(value, closure) {
    closure(closure(value))
}
println "Apply square twice to 2: ${applyTwice(2) { it * it }}"

println "\n=== 7. Closures with default arguments ==="
def repeat = { text, times = 2 -> text * times }
println repeat("Hi ")        // uses default times=2
println repeat("Hi ", 3)     // overrides default

println "\n=== 8. Closure delegation ==="
class Person {
    String name
    def introduce = { println "Hi, I'm $name" }
}

def p = new Person(name: "Tara")
p.introduce()  // delegate = p by default

def cl = { println "Delegate: ${delegate}, Owner: ${owner}, This: ${this}" }
cl()

