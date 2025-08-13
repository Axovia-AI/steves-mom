Feature: Artifacts Management
  As a user of the AI chatbot
  I want to create and manage artifacts
  So that I can generate and work with structured content

  Background:
    Given the application is running
    And I am logged in

  @smoke
  Scenario: Create a text artifact
    When I request the AI to "Create a simple HTML page about cats"
    Then an artifact should be generated
    And the artifact should be visible in the interface
    And the artifact should contain HTML content

  Scenario: Toggle artifact visibility
    Given I have created a text artifact
    When I toggle the artifact visibility
    Then the artifact should be hidden
    When I toggle the artifact visibility again
    Then the artifact should be visible again

  Scenario: Send follow-up message after artifact generation
    Given I have created an artifact
    When I send a follow-up message "Can you modify this to add more colors?"
    Then I should receive a response
    And the artifact may be updated based on the request

  @skip_unimplemented
  Scenario: Create a code artifact
    When I request the AI to "Write a Python function to calculate fibonacci numbers"
    Then a code artifact should be generated
    And the artifact should contain Python code
    And the code should be properly formatted

  @skip_unimplemented
  Scenario: Download artifact
    Given I have created an artifact
    When I click on the download artifact button
    Then the artifact content should be downloaded as a file

  @skip_unimplemented
  Scenario: Copy artifact content
    Given I have created an artifact
    When I click on the copy artifact button
    Then the artifact content should be copied to my clipboard

  @skip_unimplemented
  Scenario: Share artifact
    Given I have created an artifact
    When I click on the share artifact button
    Then I should get a shareable link to the artifact

  @skip_unimplemented
  Scenario: Edit artifact directly
    Given I have created an artifact
    When I click on the edit artifact button
    And I modify the artifact content
    And I save the changes
    Then the artifact should be updated with my changes

  @skip_unimplemented
  Scenario: Artifact version history
    Given I have created an artifact
    And I have made modifications to it
    When I view the artifact history
    Then I should see all previous versions
    And I should be able to revert to a previous version

  @skip_unimplemented
  Scenario: Multiple artifacts in one conversation
    When I request multiple artifacts in a single conversation
    Then each artifact should be created separately
    And I should be able to manage each artifact independently