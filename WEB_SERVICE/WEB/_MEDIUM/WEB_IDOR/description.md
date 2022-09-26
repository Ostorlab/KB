Insecure Direct Object Reference (IDOR) occurs when user input is not validated and directly accesses the
requested object.

Consider for instance, a website that grants access to bank account information by bank id:

```http
https://insecure-bank.com/bank/account?id=12345
```

An attacker might be able to access the information of other accounts by referencing its id.

Another manifestation of this weakness is when the id is not easily guessable, UUID, for instance, but can be
leaked through other means and used to access the object:

```http
https://insecure-bank.com/user/12/account?id=12345-abcd-12345-abcd
```
