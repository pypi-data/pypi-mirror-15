Vial
====

Vial is a simple wrapper for AES CTR mode. You have to set the key to
an appropriate length:

    AES-128bit (16 bytes/characters)
    AES-192bit (24 bytes/characters)
    AES-256bit (32 bytes/characters)

or use a hashing package that'll provide more security and ease your pain of
typing exactly the 16, 24 or 32 characters.

_Usage:_

    import vial

    vial = vial.Vial(key)
    vial.encrypt(plaintext, output_counter_file)
    vial.decrypt(plaintext, output_counter_file)
    vial.encrypt_stream(input, output, block_size)
    vial.decrypt_stream(input, output, block_size)

##### encrypt(text, counter_path)
This function needs as an extra argument a path where you want
the file with initial Counter value stored. The file is important,
you need to use it to decrypt.

_Returns:_ encrypted text (bytes)

##### decrypt(text, counter_path)
This function needs as an extra argument the path where you saved
the file from Vial.encrypt(). Without this file the text won't be
decrypted.

_Returns:_ decrypted text (bytes)

##### encrypt_stream(input, output, block_size=4096)
This function needs as extra arguments only input file and a path
for the output file. A file with Counter's initial value will be
created automatically in the same location and with the same name as
output file.

_Args:_

    input, output: Expects a file object ( f = open(...) )
    block_size (optional): The max block_size to encrypt with the same
                           AES encrypt()

_Example:_

    vial = Vial(key)
    input = open('encrypt_me.png', 'rb')
    output = open('im_encrypted.png', 'wb')
    vial.encrypt_stream(input, output)
    input.close()
    output.close()

_Result:_

    root/
        encrypt_me.png
        im_encrypted.png
        im_encrypted.ctr

##### decrypt_stream(input, output, block_size=4096)
This function needs as extra arguments only input file and a path
for the output file. The file with Counter's initial value has to be
placed in the same folder as the input file as the function
automatically checks for it and gets the value to decrypt it.

_Args:_

    input, output: Expects a file object ( f = open(...) )
    block_size (optional): The max block_size to decrypt with the same
                           AES decrypt()

_Example:_

    vial = Vial(key)
    input = open('im_encrypted.png', 'rb')
    output = open('im_decrypted.png', 'wb')
    vial.encrypt_stream(input, output)
    input.close()
    output.close()

_Result:_

    root/
        im_encrypted.png
        im_encrypted.ctr
        im_decrypted.png
