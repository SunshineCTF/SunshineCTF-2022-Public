# [CRYPTO 200(?)] AESChall

The new substitution box can be represented as a linear operation on bits, with just xors and shuffling bits. Because of this, the AES encryption operation is now an affine operation. Since you know the first block of plaintext and ciphertext you can construct a matrix and recover the key, using it to decrypt the rest of the ciphertext.
