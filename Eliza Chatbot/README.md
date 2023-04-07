# George Mason University - AIT 526 - Summer 2022 - Assignment 1 - ELIZA CHATBOT

>Welcome to Eliza, an interactive psychotherapist chatbot.

>Eliza is an interactive chatbot, designed as a psychotherapist to engage with the user with questions and respond to specific answers.  Eliza is written in Python and uses the nltk and re packages to perform NLP functions such as tokenizing, removing stop words, removing punctuation and leverages regular expressions for text matching. Eliza is able to respond to the user's answers by using word spotting for key words and by transforming certain responses into questions. Eliza will also incorporate the user's name.


Date:  June 26, 2022


### Usage Instructions

>To run Eliza, save Eliza_Team_3.py to the file system.  In your terminal, navigate to the folder where the file was saved and type

>`python Eliza_Team_3.py`

>From here, Eliza will engage the user in dialog.

>To end the conversation with Eliza, the user can enter 'Bye' or 'Quit' or 'Exit'


#### Examples

>A complete conversation example with Eliza chatbot

[Eliza] Hello! I am Eliza, your psychotherapist for the day. What is your name?
[User] Hi. I am Anna
[Eliza] Hi Anna. How are you feeling?
[Anna] I am feeling terrible
[Eliza] That isn't great. Is something bothering you?
[Anna] I cannot be successful in life
[Eliza] Why can't you be successful in life?
[Anna] I want to die
[Eliza] I'm concerned you are thinking about that. Perhaps you should call 911.
[Anna] bye
[Eliza] Bye. Have a nice day!

>Word spotting example
>In this example, Eliza is spotting the words 'terrible', 'wrong','pain', 'die' and responding accordingly

[Eliza] Hi Anna. How are you feeling?
[Anna] I feel terrible
[Eliza] That isn't great. Is something bothering you?
[Anna] Something is wrong with me.
[Eliza] Are you sure?
[Anna] I'm in pain
[Eliza] That isn't great. Is something bothering you?
[Anna] I want to die
[Eliza] I'm concerned you are thinking about that. Perhaps you should call 911.

>Sentence transformation example

[Anna] I cannot succeed in life
[Eliza] Why can't you succeed in life?
[Anna] I want to be an actor
[Eliza] Why do you want to be an actor?
[Anna] I hate you
[Eliza] Why do you hate me?

>Robustness example
>In this example, the first input from user was not detected by word-spotting or sentence transformation methods, so Eliza gave a generic reply.
>The second input was too lengthy, so Eliza asked to restate the input.
> The third input was only one word and did not match any words in the word bank, so Eliza is asking to tell more about that.

[Anna] My life is completely out of my control.
[Eliza] Could you expand on that?
[Anna] I have reached a point where taking my life seems like an only solution to me.
[Eliza] Could you restate that?
[Anna] Probably
[Eliza] Tell me more about that.

#### Additional functionality
Checking for gibberish text in the input
> Eliza checks for the gibberish text and replies appropriately

[Anna] gibberishrandom asdfjhsdjfh
[Eliza] I am not sure I understand. Could you elaborate?
[Anna] bcbvsf fhdjsdvj
[Eliza] I am not sure I understand. Could you elaborate?
[Anna] Gibberishrandom wordsarebeing inputedhere
[Eliza] I am not sure I understand. Could you elaborate?

##### Algorithm

>Eliza's questions and processing of user input follows the following algorith:

* Greet user and ask their name
  * Eliza greets the user by name and ask how they are feeling
* While the user's response is not "quit" or "bye" or "exit", Eliza processes input in the following sequence:
  * Remove contractions from the text
  * Remove punctuation from the text
  * Perform word spotting for a list of identified "dangerous" words that might indicate the user is a danger to themselves or others.  Suggest calling 911.
    * Perform regular expression matching, looking for the following matches in the following sequence and responding with the indicated format:
        * "I am feeling" or a word spotted in any of sad, happy, positive, negative word banks --> perform word spotting; get randomized response from corresponding preset list
        * "I want" --> "Why do you want ..."
        * "I can/cannot" --> "Why can't you ..."
        * "I ... you" --> "Why do ..."
     * Respond to a particularly lengthy response by asking the user to clarify
    * Analyze input for gibberish, i.e. a series of letters, numbers, or characters that are not a varifiable word
    * Respond to a one word response by asking the user to tell Elize more
    * Respond with a more generic response to the case that none of the above conditions are met

###### Troubleshooting

>If executing the command `python Eliza_Team_3.py` doesn't run as expected from a terminal and in the directory where Eliza_Team_3.py has been saved, confirm that Python has been installed.  Python installation can be verified by entering `python` at a command prompt.  A message displaying the python version installed will be displayed if python has been successfully installed.  

![Alt text](python.png "Python installed")

>If not, please install python and try again.


