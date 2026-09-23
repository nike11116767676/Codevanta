export const PRESETS = {
  java: [
    {
      id: 'java-clean',
      name: 'Clean Program',
      category: 'Working',
      description: 'Standard Java program calculating Fibonacci sequence',
      code: `public class Main {
    public static void main(String[] args) {
        int n = 10;
        int t1 = 0, t2 = 1;
        System.out.println("Fibonacci Series of " + n + " terms:");

        for (int i = 1; i <= n; ++i) {
            System.out.print(t1 + " ");
            int sum = t1 + t2;
            t1 = t2;
            t2 = sum;
        }
        System.out.println();
    }
}`
    },
    {
      id: 'java-semicolon',
      name: 'Missing Semicolon',
      category: 'Syntax Error',
      description: 'Variable declaration missing closing semicolon',
      code: `public class Main {
    public static void main(String[] args) {
        int a = 10
        int b = 20;
        System.out.println("Sum = " + (a + b));
    }
}`
    },
    {
      id: 'java-unbalanced-paren',
      name: 'Unbalanced Parentheses',
      category: 'Syntax Error',
      description: 'System.out.println call missing closing parenthesis',
      code: `public class Main {
    public static void main(String[] args) {
        String greeting = "Welcome to Codevanta";
        System.out.println(greeting;
    }
}`
    },
    {
      id: 'java-unclosed-quote',
      name: 'Unclosed String Quote',
      category: 'Syntax Error',
      description: 'String literal without terminating quotation mark',
      code: `public class Main {
    public static void main(String[] args) {
        String msg = "Hello Developer;
        System.out.println(msg);
    }
}`
    },
    {
      id: 'java-type-mismatch',
      name: 'Type Mismatch',
      category: 'Compilation Error',
      description: 'Assigning a String to an integer variable',
      code: `public class Main {
    public static void main(String[] args) {
        int value = "Codevanta";
        System.out.println(value);
    }
}`
    },
    {
      id: 'java-cannot-find-symbol',
      name: 'Undeclared Variable',
      category: 'Compilation Error',
      description: 'Using undefined variable `counter`',
      code: `public class Main {
    public static void main(String[] args) {
        int count = 5;
        System.out.println(counter * 2);
    }
}`
    },
    {
      id: 'java-div-zero',
      name: 'Division by Zero',
      category: 'Runtime Error',
      description: 'ArithmeticException division by zero',
      code: `public class Main {
    public static void main(String[] args) {
        int numerator = 100;
        int denominator = 0;
        int result = numerator / denominator;
        System.out.println(result);
    }
}`
    }
  ],
  python: [
    {
      id: 'py-clean',
      name: 'Clean Program',
      category: 'Working',
      description: 'Standard Python script calculating prime numbers',
      code: `def get_primes(limit):
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

primes_list = get_primes(30)
print(f"Primes up to 30: {primes_list}")
`
    },
    {
      id: 'py-missing-colon',
      name: 'Missing Colon',
      category: 'Syntax Error',
      description: 'if condition statement missing terminating colon',
      code: `temperature = 35

if temperature > 30
    print("It is a hot day outside.")
else:
    print("The weather is pleasant.")
`
    },
    {
      id: 'py-missing-paren',
      name: 'Unclosed Parenthesis',
      category: 'Syntax Error',
      description: 'print statement missing closing parenthesis',
      code: `score = 98
print("Final score:", score
`
    },
    {
      id: 'py-indent-error',
      name: 'Indentation Error',
      category: 'Syntax Error',
      description: 'Missing indented block inside function',
      code: `def calculate_area(width, height):
return width * height

print(calculate_area(5, 10))
`
    },
    {
      id: 'py-name-error',
      name: 'Name Error',
      category: 'Runtime Error',
      description: 'Accessing undeclared variable `total_sum`',
      code: `items = [10, 20, 30]
total = sum(items)
print("Result is:", total_sum)
`
    },
    {
      id: 'py-type-error',
      name: 'Type Error',
      category: 'Runtime Error',
      description: 'Concatenating string with integer',
      code: `age = 22
message = "Your age is: " + age
print(message)
`
    },
    {
      id: 'py-div-zero',
      name: 'Division by Zero',
      category: 'Runtime Error',
      description: 'ZeroDivisionError in calculations',
      code: `def divide(a, b):
    return a / b

val = divide(42, 0)
print("Answer:", val)
`
    }
  ]
};
