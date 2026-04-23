def print_primes(n):
    for num in range(1, n + 1):
        if num > 1:
            is_prime = True
            for i in range(2, num):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                print(num, end=" ")

# Demo
print("Prime numbers between 1 to 50: ")
print_primes(50)