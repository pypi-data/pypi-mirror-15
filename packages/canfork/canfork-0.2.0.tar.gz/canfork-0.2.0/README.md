# canfork #

Guess whether a process can fork based on its virtual memory usage and free
system memory.

+ Install via `pip install canfork`.
+ Run `canfork PID`.

# Why? #

While 

# Limitations #

Canfork currently assumes you are running with default memory overcommit
settings. However, in practice, if you aren't, then the answer to "can this
process fork?" is much simpler, and hardly requires a separate tool:

- Always overcommit: You can always fork.
- Don't overcommit: You can only fork if your virtual memory is 
  < available memory
