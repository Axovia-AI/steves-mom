Feature: Message Voting System
  As a user of the AI chatbot
  I want to vote on AI responses
  So that I can provide feedback on response quality

  Background:
    Given the application is running
    And I am logged in
    And I have sent a message and received a response

  @smoke
  Scenario: Upvote a message
    When I click the upvote button on the AI response
    Then the vote should be recorded successfully
    And the upvote button should show as selected

  @smoke
  Scenario: Downvote a message
    When I click the downvote button on the AI response
    Then the vote should be recorded successfully  
    And the downvote button should show as selected

  Scenario: Change vote from upvote to downvote
    Given I have upvoted a message
    When I click the downvote button
    Then my vote should change to downvote
    And the downvote button should show as selected
    And the upvote button should no longer be selected

  Scenario: Change vote from downvote to upvote
    Given I have downvoted a message  
    When I click the upvote button
    Then my vote should change to upvote
    And the upvote button should show as selected
    And the downvote button should no longer be selected

  @skip_unimplemented
  Scenario: Remove vote
    Given I have voted on a message
    When I click the same vote button again
    Then my vote should be removed
    And neither vote button should be selected

  @skip_unimplemented
  Scenario: View vote feedback form
    Given I have downvoted a message
    When I submit the downvote
    Then I should see a feedback form
    And I should be able to provide additional feedback

  @skip_unimplemented
  Scenario: Vote on multiple messages
    Given I have multiple AI responses in a conversation
    When I vote on different messages
    Then each vote should be recorded independently
    And I should be able to vote differently on each message

  @skip_unimplemented
  Scenario: Vote persistence across sessions
    Given I have voted on messages
    When I log out and log back in
    Then my previous votes should still be visible
    And I should not be able to vote again on the same messages

  @skip_unimplemented
  Scenario: Guest user voting limitations
    Given I am authenticated as a guest user
    When I try to vote on a message
    Then I should be prompted to register
    Or my votes should not be permanently stored

  @skip_unimplemented
  Scenario: Vote analytics for message improvement
    Given multiple users have voted on various messages
    When an administrator reviews vote data
    Then they should see aggregated voting statistics
    And be able to identify patterns in message quality