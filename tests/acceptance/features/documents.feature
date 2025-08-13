Feature: Document Management
  As a user of the AI chatbot
  I want to manage documents and files
  So that I can organize and work with my content

  Background:
    Given the application is running
    And I am logged in

  @smoke
  Scenario: Create a new document
    When I create a new document with title "My Test Document"
    And I add content "This is test content"
    Then the document should be saved successfully
    And I should be able to retrieve the document

  Scenario: Update an existing document
    Given I have created a document
    When I update the document content
    And I save the changes
    Then the document should have a new version
    And I should be able to retrieve the updated content

  Scenario: Delete a document
    Given I have created a document
    When I delete the document
    Then the document should no longer be accessible
    And it should not appear in my document list

  Scenario: Retrieve document versions
    Given I have created a document
    And I have updated it multiple times
    When I view the document history
    Then I should see all versions of the document
    And I should be able to access each version

  @skip_unimplemented
  Scenario: Share document with other users
    Given I have created a document
    When I share the document with another user
    Then the other user should be able to view the document
    But they should not be able to edit it without permission

  @skip_unimplemented
  Scenario: Collaborate on document editing
    Given I have shared a document with edit permissions
    When another user makes changes
    Then I should see the changes reflected
    And we should be able to edit simultaneously without conflicts

  @skip_unimplemented
  Scenario: Export document in different formats
    Given I have created a document
    When I export the document
    Then I should be able to choose from multiple formats
    And the exported file should contain the correct content

  @skip_unimplemented
  Scenario: Import document from file
    When I upload a document file
    Then the content should be imported into a new document
    And I should be able to edit and manage it normally

  @skip_unimplemented
  Scenario: Document search and filtering
    Given I have multiple documents
    When I search for documents by title or content
    Then I should see relevant documents in the results
    And I should be able to filter by creation date or other criteria

  @skip_unimplemented
  Scenario: Document backup and restore
    Given I have documents stored in the system
    When a backup is performed
    Then all my documents should be included
    And I should be able to restore them if needed

  Scenario: Document access permissions
    Given I have created a document
    When another user tries to access my private document
    Then they should not be able to view or edit it
    And they should receive an appropriate error message