# COSC310 - Assessment 4: TCP socket server/client v2
# Security Report
By Chris Cody - ID:220209093

## Unencrypted communication
Communication between the client and server was previously unencrypted. This meant that an attacker could intercept, read and potentially manipulate the messages sent between the client and server. This is a major security issue as the messages sent between the client and server contain sensitive information such as the user's password and the key/value pairs stored on the server. It creates potential for an attacker to implement a man-in-the-middle attack to steal the user's password and key/value pairs or manipulate data in transmission between server and client.

In the new version of this protocol, all communication between the client and server is encrypted using the RSA algorithm. The client and server exchange public keys and use these keys to encrypt messages before sending them. This prevents an attacker from intercepting and reading the encrypted messages sent between the client and server. If an attacker does intercept the communications between client and server, they will not be able to decrypt the messages without access to the private keys. These keys are randomly generated before each connection and are not hard-coded, making it difficult for an attacher to obtain the private keys.

openSSL is another option for encrypting communications that prevents the open exchange of public keys and also provides a solution to client authentication. Setting up SSL certificates is more complicated and requires additional end user setup prior to use. To make setup and marking simpler, encryption using RSA key pairs was used instead.

## Client Authentication
The original protocol did not require any client authentication. The client sent an ID to the server and was instantly connected. 

In the new version of the protocol, a client ID and password are are required on connection. The server confirms that the user exists in the database and that the password matches before a connection is established. Passwords are stored hashed (not in plaintext) and are hashed by the client prior to sending. For simplicity, the user database is hardcoded in this project, but this is a very bad idea for production code. 

In a production situation, I would recommend use of an authentication package/library to minimise any risk of introducing security issues into the user authentication system. A library can also manage secure storage of the user database, adding new users, password changes, use of MFA etc... As these libraries add significant additional complexity, I have not used on in this project. 

## Corrupted or intercepted data

TODO
To original protocol had no error detection and the client had no way of detecting if a returned value was tampered with by a bad actor. The implementation of encrypted communication in this protocol helps to increase trust by preventing a bad actor from reading sent messages. If an attacker observes a key exchange, they could potentially impersonate the client/server and send commands. 

In the second version of this protocol, command acknowledgements are implemented for several commands. These acknowlidgements 

security/privacy/trust issues that were present in your previous project submission, your approaches to mitigating those issues (which may refer to your protocol document), and how those approaches work (including any limitations). If you are unable to implement some mitigation (e.g., due to time constraints), it is recommended you still list them in the report, indicating why you were unable to implement them.