This program uses the pushbullet.py Python library, found here: https://github.com/randomchars/pushbullet.py.

This will only work on Linux operating systems.
</br></br>

<b>Dependencies</b>

You must install the pushbullet.py library to use this program, either by typing this command in the terminal:

<code>pip install pushbullet.py</code>

or downloading the source code and typing:

<code>python setup.py install</code>
</br></br>

<b>Running the Program</b>

To run this program, add your API key to the config.json file. Your API key can be found in Account Settings on the pushbullet <a href="https://www.pushbullet.com/account">site</a>.

Type this command in the terminal to run the program:

<code>python download_links.py config.json</code>

The program will run indefinitely, use the keyboard interrupt (usually CTRL-C) to quit.

Downloaded files will appear in the user's Downloads folder.
