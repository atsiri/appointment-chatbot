
# Appointment Chatbot with Rasa NLU
====================================

## About Rasa

Rasa Framework is a set of open source machine learning tools for developers to create contextual AI assistants and chatbots. It is the leading open source machine learning toolkit that lets developers expand bots beyond answering simple questions with minimal training data. The bots are based on a machine learning model trained on example conversations. 

[RASA](https://rasa.com/docs/rasa/installation/installing-rasa-open-source)

## details of this project

This is a preliminary version of Appointment Booking Agent with Rasa Open Source Framework. The project is python based appointment booking agent that can have a natural conversation with a human. The already booked slots are represented in the [appointments.csv](database/appointments.csv)

Currently the bot only able to make an appointment and checking the information of an existing booking. (More to look forward to.)

To install:
-- pip3 install rasa

Ensure the existing library also follows the set of libraries in requirements.txt.

Steps to start project after rasa installation for:
1. Download appointment-chatbot.zip and extract to open 
2. Ensure this following script is present in endpoints.yml file:

    ```
    action_endpoint:
        url: http://localhost:5055/webhook
    ```

3. Open command prompt  inside  the location folder and write command below:
    * rasa train
4. After finished training, start the rasa actions server by running this command:
    * rasa run actions
5. Open split terminal while the actions server running, and type:
    * rasa shell 
6. Say hi to your chatbot!

