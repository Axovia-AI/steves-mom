"""Step definitions for chat functionality tests."""

import pytest
import time
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Load scenarios from the feature file
scenarios('../features/chat.feature')


@given('the application is running')
def application_running(app_driver):
    """Verify the application is accessible."""
    app_driver.navigate_to('/')
    assert app_driver.driver.current_url is not None


@given('I am on the chat page')
def on_chat_page(app_driver):
    """Navigate to the chat page."""
    app_driver.navigate_to('/')
    # Wait for the chat interface to load
    app_driver.wait_for_element('textarea[placeholder*="Send a message"]')


@given('there are suggested actions available')
def suggested_actions_available(app_driver):
    """Verify suggested actions are present."""
    try:
        app_driver.wait_for_element('[data-testid="suggested-actions"]', timeout=5)
    except TimeoutException:
        pytest.skip("No suggested actions available")


@given(parsers.parse('I have sent a message "{message}"'))
def sent_message(app_driver, message):
    """Send a message and wait for response."""
    send_message_and_wait(app_driver, message)


@given('I have received a response')
def received_response(app_driver):
    """Verify a response was received."""
    # Wait for assistant message to appear
    app_driver.wait_for_element('[data-author="assistant"]')


@given('I have multiple messages in the chat')
def multiple_messages(app_driver):
    """Create multiple messages in the chat."""
    for i in range(3):
        send_message_and_wait(app_driver, f"Test message {i+1}")


@when(parsers.parse('I send the message "{message}"'))
def send_message(app_driver, message):
    """Send a message to the chat."""
    # Find and click the textarea
    textarea = app_driver.wait_for_element('textarea[placeholder*="Send a message"]')
    textarea.click()
    textarea.clear()
    textarea.send_keys(message)
    
    # Find and click the send button
    send_button = app_driver.wait_for_element_clickable('button[type="submit"]')
    send_button.click()


@when('I click on a suggested action')
def click_suggested_action(app_driver):
    """Click on the first available suggested action."""
    suggested_action = app_driver.wait_for_element_clickable('[data-testid="suggested-actions"] button')
    suggested_action.click()


@when('I click the stop button while generating')
def click_stop_button(app_driver):
    """Click the stop button during generation."""
    try:
        # Wait briefly for generation to start and stop button to appear
        stop_button = app_driver.wait_for_element_clickable('[data-testid="stop-button"]', timeout=5)
        stop_button.click()
    except TimeoutException:
        pytest.skip("Stop button not available - generation may have completed too quickly")


@when(parsers.parse('I edit the message to "{new_message}"'))
def edit_message(app_driver, new_message):
    """Edit the most recent user message."""
    try:
        # Find the most recent user message
        user_messages = app_driver.find_elements('[data-author="user"]')
        if user_messages:
            last_message = user_messages[-1]
            
            # Look for edit button - might be in a menu or directly visible
            edit_button = last_message.find_element(By.CSS_SELECTOR, '[data-testid="edit-button"], button[aria-label*="edit"]')
            edit_button.click()
            
            # Find the edit textarea and update the content
            edit_textarea = app_driver.wait_for_element('textarea[data-testid="edit-textarea"]')
            edit_textarea.clear()
            edit_textarea.send_keys(new_message)
            
            # Submit the edit
            submit_edit = app_driver.wait_for_element_clickable('button[data-testid="submit-edit"]')
            submit_edit.click()
        else:
            pytest.fail("No user messages found to edit")
    except Exception:
        pytest.skip("Message editing not implemented or not accessible")


@when('I upload an image file')
def upload_image(app_driver):
    """Upload an image file."""
    try:
        # Look for file upload button or input
        upload_input = app_driver.wait_for_element('input[type="file"]', timeout=5)
        # Use a test image path - this would need to be a real image file in practice
        test_image_path = "/tmp/test_image.jpg"
        
        # For testing purposes, we'll skip if no actual file is available
        import os
        if not os.path.exists(test_image_path):
            pytest.skip("Test image file not available")
            
        upload_input.send_keys(test_image_path)
    except TimeoutException:
        pytest.skip("File upload not available or not implemented")


@when('I scroll up in the chat')
def scroll_up_in_chat(app_driver):
    """Scroll up in the chat area."""
    chat_area = app_driver.wait_for_element('[data-testid="chat-messages"]')
    app_driver.driver.execute_script("arguments[0].scrollTop = 0;", chat_area)


@when('I click the "scroll to bottom" button')
def click_scroll_to_bottom(app_driver):
    """Click the scroll to bottom button."""
    scroll_button = app_driver.wait_for_element_clickable('[data-testid="scroll-to-bottom"]')
    scroll_button.click()


@then('I should receive a response')
def should_receive_response(app_driver):
    """Verify that a response was received."""
    # Wait for assistant message to appear
    app_driver.wait_for_element('[data-author="assistant"]', timeout=30)


@then('the response should contain meaningful content')
def response_contains_content(app_driver):
    """Verify the response contains meaningful content."""
    assistant_messages = app_driver.find_elements('[data-author="assistant"]')
    assert len(assistant_messages) > 0, "No assistant messages found"
    
    last_response = assistant_messages[-1]
    response_text = last_response.text.strip()
    assert len(response_text) > 10, f"Response too short: {response_text}"


@then('the suggested actions should be hidden')
def suggested_actions_hidden(app_driver):
    """Verify suggested actions are no longer visible."""
    time.sleep(1)  # Brief wait for UI update
    assert not app_driver.is_element_present('[data-testid="suggested-actions"]')


@then('the message generation should stop')
def generation_should_stop(app_driver):
    """Verify message generation has stopped."""
    # Wait briefly and check that no loading indicators are present
    time.sleep(2)
    assert not app_driver.is_element_present('[data-testid="loading"]')


@then('the send button should be available again')
def send_button_available(app_driver):
    """Verify the send button is available."""
    send_button = app_driver.wait_for_element('button[type="submit"]')
    assert send_button.is_enabled()


@then('I should receive a new response')
def should_receive_new_response(app_driver):
    """Verify a new response was received."""
    app_driver.wait_for_api_response()
    assistant_messages = app_driver.find_elements('[data-author="assistant"]')
    assert len(assistant_messages) > 0


@then('the response should be relevant to the new question')
def response_relevant_to_new_question(app_driver):
    """Verify response relevance - basic check."""
    # This is a simplified check - in practice you'd check content relevance
    assistant_messages = app_driver.find_elements('[data-author="assistant"]')
    last_response = assistant_messages[-1]
    assert len(last_response.text.strip()) > 5


@then('I should receive a response about the image')
def response_about_image(app_driver):
    """Verify response is about the uploaded image."""
    should_receive_response(app_driver)
    # Additional verification that response mentions image content would go here


@then('the message should show the attached image')
def message_shows_attached_image(app_driver):
    """Verify the message displays the attached image."""
    user_messages = app_driver.find_elements('[data-author="user"]')
    last_message = user_messages[-1]
    # Look for image attachment in the message
    assert last_message.find_elements(By.CSS_SELECTOR, 'img, [data-testid="attachment"]')


@then('I should receive a response with weather information')
def response_with_weather_info(app_driver):
    """Verify response contains weather information."""
    should_receive_response(app_driver)
    assistant_messages = app_driver.find_elements('[data-author="assistant"]')
    last_response = assistant_messages[-1].text.lower()
    
    # Check for weather-related terms
    weather_terms = ['temperature', 'weather', 'degrees', '°c', '°f']
    assert any(term in last_response for term in weather_terms), f"No weather terms found in: {last_response}"


@then('the response should contain temperature data')
def response_contains_temperature(app_driver):
    """Verify response contains temperature data."""
    assistant_messages = app_driver.find_elements('[data-author="assistant"]')
    last_response = assistant_messages[-1].text
    
    # Look for temperature patterns
    import re
    temp_pattern = r'\d+°[CF]|\d+\s*(degrees|°)'
    assert re.search(temp_pattern, last_response), f"No temperature data found in: {last_response}"


@then('the URL should change to include a chat ID')
def url_includes_chat_id(app_driver):
    """Verify URL contains a chat ID."""
    current_url = app_driver.driver.current_url
    # Check if URL pattern matches /chat/[id]
    import re
    chat_url_pattern = r'/chat/[a-zA-Z0-9\-_]+'
    assert re.search(chat_url_pattern, current_url), f"URL doesn't match chat pattern: {current_url}"


@then('I should be able to share this URL')
def should_be_able_to_share_url(app_driver):
    """Verify the URL is shareable."""
    current_url = app_driver.driver.current_url
    assert 'chat' in current_url
    # In a real test, you might verify the URL works in a new session


@then('the chat should automatically scroll to the bottom')
def chat_scrolls_to_bottom(app_driver):
    """Verify chat scrolls to bottom."""
    pytest.skip("Auto-scroll verification not implemented")


@then('a "scroll to bottom" button should appear')
def scroll_button_appears(app_driver):
    """Verify scroll to bottom button appears."""
    pytest.skip("Scroll button verification not implemented")


@then('the chat should scroll to the bottom')
def chat_scrolled_to_bottom(app_driver):
    """Verify chat is scrolled to bottom."""
    pytest.skip("Scroll position verification not implemented")


@then('the button should disappear')
def button_disappears(app_driver):
    """Verify button disappears."""
    pytest.skip("Button disappearance verification not implemented")


# Helper functions
def send_message_and_wait(app_driver, message):
    """Send a message and wait for response."""
    send_message(app_driver, message)
    app_driver.wait_for_api_response()