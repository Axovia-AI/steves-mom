Feature: Authentication and Session Management
  As a user of the AI chatbot
  I want to manage my authentication and sessions
  So that I can have personalized and secure interactions

  @smoke
  Scenario: Guest user authentication
    Given I am not logged in
    When I visit the application
    Then I should be automatically authenticated as a guest user
    And I should be able to start chatting immediately

  Scenario: User registration
    Given I am not logged in
    When I navigate to the registration page
    And I fill in valid registration details
    And I submit the registration form
    Then I should be successfully registered
    And I should be logged in

  Scenario: User login
    Given I have a registered account
    And I am not logged in
    When I navigate to the login page
    And I enter my valid credentials
    And I submit the login form
    Then I should be successfully logged in
    And I should see my email in the user menu

  Scenario: User logout
    Given I am logged in as a registered user
    When I click on the user menu
    And I select logout
    Then I should be logged out
    And I should be redirected to the guest session

  Scenario: Guest user limitations - message limit
    Given I am authenticated as a guest user
    When I send 20 messages
    Then I should reach the daily message limit
    And I should be prompted to register

  @skip_unimplemented
  Scenario: Session persistence across browser refresh
    Given I am logged in as a registered user
    And I have an active chat session
    When I refresh the browser
    Then I should remain logged in
    And my chat session should be preserved

  Scenario: Navigation restrictions for guest users
    Given I am authenticated as a guest user
    When I try to access protected features
    Then I should be able to access basic chat functionality
    But I should have limited access to advanced features

  Scenario: Navigation restrictions for authenticated users
    Given I am logged in as a registered user
    When I try to access the login page
    Then I should be redirected away from the login page
    When I try to access the registration page  
    Then I should be redirected away from the registration page

  @skip_unimplemented
  Scenario: Account recovery
    Given I have a registered account
    And I have forgotten my password
    When I request a password reset
    Then I should receive a password reset email
    And I should be able to reset my password

  @skip_unimplemented
  Scenario: Session timeout
    Given I am logged in as a registered user
    When I remain inactive for an extended period
    Then my session should expire
    And I should be prompted to log in again