# diffie-helman
Project for my Intro to Network Security class, using the popular Diffie-Helman method for creating keys for secure communication.

For dh.py: 
You will need to run this program on two tabs, which will be "Cam" and "Sam" attempting to speak to one another. Navigate to the file, then type "python dh.py --c localhost", open a new tab in terminal, then type "python dh.py --s". This should then display a long string of numbers, which is the key created by the algorithm. 

For signer.py: 
On the first tab in terminal (or whatever program you wish to use), you will need to navigate to this file and then type "python signer.py --c localhost --message". On the second tab, you then type "python signer.py --s" (after making sure you have navigated to the file). This should authenticate the signed version of the message. 

If you wish to display print messages, you may need to un-comment the tests I wrote in the files. The specifics of the algorithms should be clear in the comments of the files, but I can always be reached for questions at md1341@georgetown.edu.

The images included, as indicated by the names, demonstrate how the program works. 
