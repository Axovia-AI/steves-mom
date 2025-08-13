Feature: Reasoning Mode
  As a user of the AI chatbot
  I want to use reasoning mode for complex problems
  So that I can see the AI's thought process and get better answers

  Background:
    Given the application is running
    And I am logged in with reasoning mode enabled

  @smoke
  Scenario: Send message in reasoning mode
    When I send the message "Solve this logic puzzle: Three friends each have a different pet"
    Then I should receive a response with reasoning
    And the reasoning section should be visible
    And the reasoning should show step-by-step thinking

  Scenario: Toggle reasoning visibility
    Given I have received a response with reasoning
    When I toggle the reasoning visibility
    Then the reasoning section should be hidden
    When I toggle the reasoning visibility again
    Then the reasoning section should be visible

  Scenario: Edit message and resubmit in reasoning mode
    Given I have sent a message in reasoning mode
    And I have received a response with reasoning
    When I edit the message to ask a different question
    Then I should receive a new response with updated reasoning
    And the reasoning should be relevant to the new question

  @skip_unimplemented
  Scenario: Compare reasoning vs normal mode
    Given I send the same message in normal mode
    And I send the same message in reasoning mode
    Then the reasoning mode response should include thinking steps
    And the reasoning mode response may be more detailed

  @skip_unimplemented
  Scenario: Reasoning mode for mathematical problems
    When I send a complex math problem in reasoning mode
    Then the reasoning should show mathematical steps
    And each calculation step should be clearly explained

  @skip_unimplemented
  Scenario: Reasoning mode for coding problems
    When I ask for help with a coding problem in reasoning mode
    Then the reasoning should show problem analysis
    And the approach to solving the coding problem

  @skip_unimplemented
  Scenario: Reasoning mode settings and preferences
    When I access reasoning mode settings
    Then I should be able to customize reasoning display
    And set preferences for reasoning detail level

  @skip_unimplemented
  Scenario: Export reasoning trace
    Given I have received responses with reasoning
    When I export the reasoning trace
    Then I should get a formatted document with all reasoning steps
    And it should be useful for learning or documentation

  @skip_unimplemented
  Scenario: Reasoning mode performance impact
    When I use reasoning mode extensively
    Then the responses should still be delivered in reasonable time
    And the interface should remain responsive

  @skip_unimplemented
  Scenario: Reasoning mode with follow-up questions
    Given I have received a response with reasoning
    When I ask a follow-up question about the reasoning
    Then the AI should be able to clarify its thinking process
    And provide additional reasoning if needed