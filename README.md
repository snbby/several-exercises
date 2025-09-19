## General info
I used `uv` for package management  
`httpx` for async requests  
`pytest` for testing 


## Installation
```
git clone git@github.com:snbby/several-exercises.git
cd several-exercises
uv sync
```

## Run tests
```
uv run pytest
```

## Thoughts
### Concurrency exercise
I decided the concurrent function to return dict with results.  
We can just return the list of responses/errors in the same order the urls were provided, but in my opinion it will require more boilerplate to handle these results.  
Retry wrapper logic can be added additionally (let's say 3 retries with exponential backoff).  


### License plate problem
Complexity of the calculation is O(1).  
You can view the maximum generatable number in the tests.