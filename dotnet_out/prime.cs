```csharp
using System;

class Program
{
    static void Main()
    {
        int n, i, flag = 0;

        Console.Write("Enter a number: ");
        n = Convert.ToInt32(Console.ReadLine());

        if (n <= 1)
        {
            flag = 1;
        }
        else
        {
            for (i = 2; i <= n / 2; i++)
            {
                if (n % i == 0)
                {
                    flag = 1;
                    break;
                }
            }
        }

        if (flag == 0)
            Console.WriteLine($"{n} is a Prime Number");
        else
            Console.WriteLine($"{n} is NOT a Prime Number");
    }
}
```