Feature: Chat Functionality
  As a user of the AI chatbot
  I want to send messages and receive responses
  So that I can have conversations with the AI

  Background:
    Given the application is running
    And I am on the chat page

  @smoke
  Scenario: Send a basic message and receive response
    When I send the message "Why is grass green?"
    Then I should receive a response
    And the response should contain meaningful content

  @smoke  
  Scenario: Send message from suggestion
    Given there are suggested actions available
    When I click on a suggested action
    Then I should receive a response
    And the suggested actions should be hidden

  Scenario: Stop message generation
    When I send the message "Why is grass green?"
    And I click the stop button while generating
    Then the message generation should stop
    And the send button should be available again

  Scenario: Edit and resubmit message
    Given I have sent a message "Why is grass green?"
    And I have received a response
    When I edit the message to "Why is the sky blue?"
    Then I should receive a new response
    And the response should be relevant to the new question

  Scenario: Upload image attachment
    When I upload an image file
    And I send the message "Who painted this?"
    Then I should receive a response about the image
    And the message should show the attached image

  @skip_unimplemented
  Scenario: Send multiple messages in conversation
    Given I have sent a message "What is machine learning?"
    And I have received a response
    When I send a follow-up message "Can you give me an example?"
    Then I should receive a response that references the previous context

  Scenario: Weather tool integration
    When I send the message "What's the weather in sf?"
    Then I should receive a response with weather information
    And the response should contain temperature data

  Scenario: Redirect to chat ID after sending message
    When I send the message "Hello"
    Then the URL should change to include a chat ID
    And I should be able to share this URL

  @skip_unimplemented
  Scenario: Auto-scroll to bottom during conversation
    Given I have multiple messages in the chat
    When I send a new message
    Then the chat should automatically scroll to the bottom

  @skip_unimplemented  
  Scenario: Scroll to bottom button functionality
    Given I have multiple messages in the chat
    When I scroll up in the chat
    Then a "scroll to bottom" button should appear
    When I click the "scroll to bottom" button
    Then the chat should scroll to the bottom
    And the button should disappear