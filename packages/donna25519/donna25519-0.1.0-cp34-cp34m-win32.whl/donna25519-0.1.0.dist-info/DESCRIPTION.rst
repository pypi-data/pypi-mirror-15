Curve 25519 is an elliptic curve cryptography key-agreement protocol.

Two parties, Alice and Bob, first generate their (public, private) 
keypairs. They then exchange public keys on an insecure channel, and 
use the protocol to establish a shared secret between them.

This is a Python wrapper for the 'curve25519-donna' library for the 
curve 25519 elliptic curve Diffie-Hellman key exchange algorithm. The
portable C 'Donna' library was written by Adam Langley, and is hosted 
at https://github.com/agl/curve25519-donna. This library is a near-
complete rewrite of an earlier python wrapper written by Brian Warner 
of Mozilla.

Documentation is available at https://github.com/Muterra/curve25519-donna.


