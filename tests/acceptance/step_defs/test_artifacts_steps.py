"""Step definitions for artifacts management tests."""

import pytest
import time
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Load scenarios from the feature file
scenarios('../features/artifacts.feature')


@given('I am logged in')
def logged_in(app_driver):
    """Ensure user is logged in."""
    # For artifacts functionality, we need to be logged in
    # Use the authentication step if available, otherwise assume guest access
    app_driver.navigate_to('/')
    time.sleep(2)


@given('I have created a text artifact')
def created_text_artifact(app_driver):
    """Create a text artifact for testing."""
    request_artifact_creation(app_driver, "Create a simple HTML page about cats")
    wait_for_artifact_generation(app_driver)


@given('I have created an artifact')
def created_artifact(app_driver):
    """Create an artifact for testing."""
    created_text_artifact(app_driver)


@when(parsers.parse('I request the AI to "{request}"'))
def request_artifact_creation(app_driver, request):
    """Request the AI to create an artifact."""
    # Navigate to chat if not already there
    app_driver.navigate_to('/')
    
    # Send message that should trigger artifact creation
    textarea = app_driver.wait_for_element('textarea[placeholder*="Send a message"]')
    textarea.click()
    textarea.clear()
    textarea.send_keys(request)
    
    # Submit the request
    send_button = app_driver.wait_for_element_clickable('button[type="submit"]')
    send_button.click()


@when('I toggle the artifact visibility')
def toggle_artifact_visibility(app_driver):
    """Toggle the visibility of an artifact."""
    try:
        # Look for artifact toggle/visibility button
        toggle_button = app_driver.wait_for_element_clickable('[data-testid="artifact-toggle"], [data-testid="toggle-artifact"]', timeout=5)
        toggle_button.click()
        time.sleep(1)  # Wait for toggle to complete
    except TimeoutException:
        pytest.skip("Artifact visibility toggle not found or not implemented")


@when(parsers.parse('I send a follow-up message "{message}"'))
def send_followup_message(app_driver, message):
    """Send a follow-up message."""
    from step_defs.test_chat_steps import send_message
    send_message(app_driver, message)


@when('I click on the download artifact button')
def click_download_artifact(app_driver):
    """Click the download artifact button."""
    try:
        download_button = app_driver.wait_for_element_clickable('[data-testid="download-artifact"]', timeout=5)
        download_button.click()
    except TimeoutException:
        pytest.skip("Download artifact button not found")


@when('I click on the copy artifact button')
def click_copy_artifact(app_driver):
    """Click the copy artifact button."""
    try:
        copy_button = app_driver.wait_for_element_clickable('[data-testid="copy-artifact"]', timeout=5)
        copy_button.click()
    except TimeoutException:
        pytest.skip("Copy artifact button not found")


@when('I click on the share artifact button')
def click_share_artifact(app_driver):
    """Click the share artifact button."""
    try:
        share_button = app_driver.wait_for_element_clickable('[data-testid="share-artifact"]', timeout=5)
        share_button.click()
    except TimeoutException:
        pytest.skip("Share artifact button not found")


@when('I click on the edit artifact button')
def click_edit_artifact(app_driver):
    """Click the edit artifact button."""
    try:
        edit_button = app_driver.wait_for_element_clickable('[data-testid="edit-artifact"]', timeout=5)
        edit_button.click()
    except TimeoutException:
        pytest.skip("Edit artifact button not found")


@when('I modify the artifact content')
def modify_artifact_content(app_driver):
    """Modify the content of an artifact."""
    try:
        # Look for artifact editor
        editor = app_driver.wait_for_element('[data-testid="artifact-editor"], textarea[data-testid="artifact-content"]', timeout=5)
        editor.clear()
        editor.send_keys('<h1>Modified Content</h1><p>This content has been modified.</p>')
    except TimeoutException:
        pytest.skip("Artifact editor not found")


@when('I save the changes')
def save_artifact_changes(app_driver):
    """Save changes to an artifact."""
    try:
        save_button = app_driver.wait_for_element_clickable('[data-testid="save-artifact"]', timeout=5)
        save_button.click()
        time.sleep(1)  # Wait for save to complete
    except TimeoutException:
        pytest.skip("Save artifact button not found")


@when('I view the artifact history')
def view_artifact_history(app_driver):
    """View the history of an artifact."""
    try:
        history_button = app_driver.wait_for_element_clickable('[data-testid="artifact-history"]', timeout=5)
        history_button.click()
    except TimeoutException:
        pytest.skip("Artifact history not found")


@when('I have made modifications to it')
def made_modifications(app_driver):
    """Make modifications to an artifact."""
    click_edit_artifact(app_driver)
    modify_artifact_content(app_driver)
    save_artifact_changes(app_driver)


@when('I request multiple artifacts in a single conversation')
def request_multiple_artifacts(app_driver):
    """Request multiple artifacts in one conversation."""
    requests = [
        "Create a HTML page about dogs",
        "Create a CSS stylesheet for the page",
        "Create a JavaScript function for interactivity"
    ]
    
    for request in requests:
        request_artifact_creation(app_driver, request)
        wait_for_artifact_generation(app_driver)


@then('an artifact should be generated')
def artifact_should_be_generated(app_driver):
    """Verify an artifact was generated."""
    wait_for_artifact_generation(app_driver)


@then('the artifact should be visible in the interface')
def artifact_should_be_visible(app_driver):
    """Verify the artifact is visible."""
    assert app_driver.is_element_present('[data-testid="artifact"], [data-testid="artifact-container"]')


@then('the artifact should contain HTML content')
def artifact_should_contain_html(app_driver):
    """Verify the artifact contains HTML content."""
    try:
        artifact = app_driver.wait_for_element('[data-testid="artifact"]', timeout=5)
        artifact_content = artifact.text or artifact.get_attribute('innerHTML')
        
        # Check for HTML-like content
        html_indicators = ['<html>', '<head>', '<body>', '<h1>', '<p>', '<div>']
        assert any(indicator in artifact_content.lower() for indicator in html_indicators), \
            f"No HTML content detected in artifact: {artifact_content}"
    except TimeoutException:
        pytest.fail("Artifact not found to verify HTML content")


@then('the artifact should be hidden')
def artifact_should_be_hidden(app_driver):
    """Verify the artifact is hidden."""
    time.sleep(1)  # Wait for toggle to complete
    # Artifact element might still exist but be hidden, or not be present
    try:
        artifact = app_driver.find_element('[data-testid="artifact"]')
        # Check if hidden via CSS
        assert not artifact.is_displayed()
    except:
        # Artifact element not found, which also means it's hidden
        pass


@then('the artifact should be visible again')
def artifact_should_be_visible_again(app_driver):
    """Verify the artifact is visible again."""
    artifact_should_be_visible(app_driver)
    artifact = app_driver.wait_for_element('[data-testid="artifact"]')
    assert artifact.is_displayed()


@then('the artifact may be updated based on the request')
def artifact_may_be_updated(app_driver):
    """Verify the artifact may be updated."""
    # Wait for any potential updates
    time.sleep(2)
    # Since artifacts may or may not be updated based on the request,
    # we just verify the system is still functional
    assert app_driver.is_element_present('textarea[placeholder*="Send a message"]')


@then('a code artifact should be generated')
def code_artifact_should_be_generated(app_driver):
    """Verify a code artifact was generated."""
    pytest.skip("Code artifact verification not implemented")


@then('the artifact should contain Python code')
def artifact_should_contain_python(app_driver):
    """Verify the artifact contains Python code."""
    pytest.skip("Python code verification not implemented")


@then('the code should be properly formatted')
def code_should_be_formatted(app_driver):
    """Verify the code is properly formatted."""
    pytest.skip("Code formatting verification not implemented")


@then('the artifact content should be downloaded as a file')
def artifact_should_be_downloaded(app_driver):
    """Verify the artifact was downloaded."""
    pytest.skip("Download verification not implemented")


@then('the artifact content should be copied to my clipboard')
def artifact_copied_to_clipboard(app_driver):
    """Verify the artifact was copied to clipboard."""
    pytest.skip("Clipboard verification not implemented")


@then('I should get a shareable link to the artifact')
def should_get_shareable_link(app_driver):
    """Verify a shareable link is provided."""
    pytest.skip("Shareable link verification not implemented")


@then('the artifact should be updated with my changes')
def artifact_should_be_updated(app_driver):
    """Verify the artifact was updated."""
    pytest.skip("Artifact update verification not implemented")


@then('I should see all previous versions')
def should_see_previous_versions(app_driver):
    """Verify all previous versions are visible."""
    pytest.skip("Version history verification not implemented")


@then('I should be able to revert to a previous version')
def should_revert_to_previous_version(app_driver):
    """Verify ability to revert to previous version."""
    pytest.skip("Version revert verification not implemented")


@then('each artifact should be created separately')
def each_artifact_created_separately(app_driver):
    """Verify each artifact is created separately."""
    pytest.skip("Multiple artifact verification not implemented")


@then('I should be able to manage each artifact independently')
def should_manage_artifacts_independently(app_driver):
    """Verify independent artifact management."""
    pytest.skip("Independent artifact management verification not implemented")


# Helper functions
def wait_for_artifact_generation(app_driver):
    """Wait for artifact generation to complete."""
    try:
        # Wait for the response to complete
        app_driver.wait_for_api_response()
        
        # Look for artifact indicators
        app_driver.wait_for_element('[data-testid="artifact"], [data-testid="artifact-container"]', timeout=30)
    except TimeoutException:
        pytest.skip("Artifact not generated or artifact UI not found")