# Have I Been Pwned?

Python interface to Have I Been Pwned API


## What is Have I Been Pwned?

[Have I Been Pwned](https://haveibeenpwned.com/) is a free resource to quickly assess if an account or domain has been compromised or "pwned" in a data breach. By aggregating the data here the project helps victims be aware of account compromises, and highlights the severity of the risks of Internet-wide attacks. For more information on who, what, and why, click [here](https://haveibeenpwned.com/About).

## Dependencies

```
requests
gevent
```

## Setup

This library runs on **Python3.x+**

To install, run:

```
$ pip install hibp
```

## To run

You can query breach data on individual accounts/domains as well as data on full breaches. Each service request object contains a response attribute that holds the raw data output in JSON format. To perform a query, just setup a service request object, and then execute:

```python
>> req = HIBP.get_account_breaches("pegasos1")
>> req.execute()
>> req.response
```


If you want to query on multiple accounts or domains at once, you can use the `AsyncHIBP` object, which performs queries concurrently via gevent.

```python
>> names = ['adobe','ashleymadison', 'myspace']
>> breaches = [HIBP.get_breach(x) for x in names]
>> async_reqs = AsyncHIBP().map(breaches)
>> [async_req.response for async_req in async_reqs]
```

In addition to a canonical `map` method, `AsyncHIBP` also supports the `imap` method, which returns a generator object for lazy queries.


```python
>> domains = ['twitter.com','facebook.com', 'adobe.com']
>> breaches = [HIBP.get_domain_breaches(x) for x in domains]
>> async_reqs = AsyncHIBP().imap(breaches)
>> next(async_reqs)
```


