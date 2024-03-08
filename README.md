# Data-Tool
This is a repo to help find if a message being sent to a chat bot contains pii data or not. It uses a mix of Regular Expression and database scanning to work this out.

## Installation process
To install and use the data tool you will need to clone down this repo to your local machine. 
1. Open the command line and navigate to the folder you wish to install the data-tool in.
2. Ensure you have git installed and run the following command: `git clone https://github.com/AaronAubeck/data-tool.git`
3. Navigate into the data-tool folder

You will have now successfully downloaded the data-tool repo onto your local machine. You would now need to use pip to install the required environments. When creating the tool I did this inside a virtual environment using pythons `virtualenv` package. This is completely optional and can be done without this step.

Once in the data-tool folder run the following command in the command line to install the tools python package requirements: `pip install -r development\requirements.txt`. This may take a few minutes to install all the necessary requirements. Once it has finished you can run `pip freeze` to ensure all the packages have successfully installed.

Congratulations! You have successfully installed the data-tool onto your machine and are ready to start checking for pii data.

## Usage/Examples

To run the data-tool you will need an open command line. If you have followed all the steps above you should already have one open and have navigatied to the data-tools repo. You will now need to run `python development\scripts\main.py` or navigate into the `development\scripts` folder and run `python main.py`.

You will now be prompted in the command line '*Please type your message you wish to ask a chat bot.*'

![Command line example of data-tool start up](image.png)

Type (or copy+paste) any text you would like to be checked before sending to a chat bot. 

### Safe Example
This example shows the user having asked the chat bot to generate a picture of a christmas tree. 
![Example not including pii data](image-1.png)

Because there is no pii data in the request the data-tool correctly returned that the provided text was safe to send to a chat bot.

### Unsafe Example (contains PII data)

In this example the user is asking to generate an email to send to a user. This would be safe but they included the email in the message.

![Example including pii data](image-2.png)

The data-tool was able to correctly highlight there was an email included in the provided text. It then asks if the user wishes to see the data in case they are unsure what pii data was included. In this instance the user asked to see the pii data.

![Showing the pii data](image-3.png)

The data-tool was able to correctly display the pii data to the user for removal.

## Test

Some test cases were written to prove the functionality of the data-tool works as expected. These can be found in the testing/tests folder.

To run these you will first need to install the test requirements. 

1. Open the command line and navigate to the data-tool folder. Please see the Installation Process above if you do not have this repo installed.
2. Run the following command: `pip install -r testing\test_requirements.txt`
3. Once these have installed run the following command: `pytest --cov main`

Running this should get you the following output:

```
---------- coverage: platform win32, python 3.11.0-final-0 -----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
development\scripts\main.py      74     30    59%
-------------------------------------------------
TOTAL                            74     30    59%
```
