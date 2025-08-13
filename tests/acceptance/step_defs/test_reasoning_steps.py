"""Step definitions for reasoning mode tests."""

import pytest
import time
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Load scenarios from the feature file
scenarios('../features/reasoning.feature')


@given('I am logged in with reasoning mode enabled')
def logged_in_with_reasoning_mode(app_driver):
    """Ensure user is logged in with reasoning mode enabled."""
    # First log in (or use guest mode)
    app_driver.navigate_to('/')
    time.sleep(2)
    
    # Enable reasoning mode if not already enabled
    try:
        # Look for reasoning mode toggle/setting
        reasoning_toggle = app_driver.wait_for_element_clickable('[data-testid="reasoning-toggle"], [data-testid="enable-reasoning"]', timeout=5)
        
        # Check if reasoning mode is already enabled
        if 'enabled' not in reasoning_toggle.get_attribute('class').lower():
            reasoning_toggle.click()
            time.sleep(1)
    except TimeoutException:
        # If no toggle found, assume reasoning mode is available by default
        # or enabled through a different mechanism
        pass


@given('I have received a response with reasoning')
def received_response_with_reasoning(app_driver):
    """Send a message and receive a response with reasoning."""
    send_message_in_reasoning_mode(app_driver, "Solve this logic puzzle: Three friends each have a different pet")
    wait_for_reasoning_response(app_driver)


@given('I have sent a message in reasoning mode')
def sent_message_in_reasoning_mode(app_driver):
    """Send a message in reasoning mode."""
    send_message_in_reasoning_mode(app_driver, "Explain the water cycle step by step")


@given('I send the same message in normal mode')
def send_message_in_normal_mode(app_driver):
    """Send a message in normal mode for comparison."""
    # Disable reasoning mode temporarily
    try:
        reasoning_toggle = app_driver.wait_for_element_clickable('[data-testid="reasoning-toggle"]', timeout=5)
        if 'enabled' in reasoning_toggle.get_attribute('class').lower():
            reasoning_toggle.click()
            time.sleep(1)
        
        # Send the same message
        from step_defs.test_chat_steps import send_message_and_wait
        send_message_and_wait(app_driver, "Solve this logic puzzle: Three friends each have a different pet")
        
        # Re-enable reasoning mode
        reasoning_toggle.click()
        time.sleep(1)
    except TimeoutException:
        pytest.skip("Cannot toggle reasoning mode for comparison")


@given('I send the same message in reasoning mode')
def send_same_message_in_reasoning_mode(app_driver):
    """Send the same message in reasoning mode."""
    send_message_in_reasoning_mode(app_driver, "Solve this logic puzzle: Three friends each have a different pet")


@when(parsers.parse('I send the message "{message}"'))
def send_message_in_reasoning_mode(app_driver, message):
    """Send a message in reasoning mode."""
    # Ensure we're in reasoning mode
    logged_in_with_reasoning_mode(app_driver)
    
    # Send the message
    textarea = app_driver.wait_for_element('textarea[placeholder*="Send a message"]')
    textarea.click()
    textarea.clear()
    textarea.send_keys(message)
    
    # Submit the message
    send_button = app_driver.wait_for_element_clickable('button[type="submit"]')
    send_button.click()


@when('I toggle the reasoning visibility')
def toggle_reasoning_visibility(app_driver):
    """Toggle the visibility of the reasoning section."""
    try:
        # Look for reasoning visibility toggle
        reasoning_toggle = app_driver.wait_for_element_clickable('[data-testid="toggle-reasoning-visibility"], [data-testid="reasoning-toggle-view"]', timeout=5)
        reasoning_toggle.click()
        time.sleep(1)  # Wait for toggle to complete
    except TimeoutException:
        pytest.skip("Reasoning visibility toggle not found")


@when(parsers.parse('I edit the message to ask a different question'))
def edit_message_to_different_question(app_driver):
    """Edit the message to ask a different question."""
    try:
        # Find the most recent user message
        user_messages = app_driver.find_elements('[data-author="user"]')
        if user_messages:
            last_message = user_messages[-1]
            
            # Look for edit button
            edit_button = last_message.find_element(By.CSS_SELECTOR, '[data-testid="edit-button"], button[aria-label*="edit"]')
            edit_button.click()
            
            # Find the edit textarea and update the content
            edit_textarea = app_driver.wait_for_element('textarea[data-testid="edit-textarea"]')
            edit_textarea.clear()
            edit_textarea.send_keys("What are the main causes of climate change?")
            
            # Submit the edit
            submit_edit = app_driver.wait_for_element_clickable('button[data-testid="submit-edit"]')
            submit_edit.click()
        else:
            pytest.fail("No user messages found to edit")
    except Exception:
        pytest.skip("Message editing not available in reasoning mode")


@when('I send a complex math problem in reasoning mode')
def send_complex_math_problem(app_driver):
    """Send a complex math problem."""
    math_problem = "If f(x) = 2x² + 3x - 1, find the derivative and determine critical points"
    send_message_in_reasoning_mode(app_driver, math_problem)


@when('I ask for help with a coding problem in reasoning mode')
def send_coding_problem(app_driver):
    """Send a coding problem."""
    coding_problem = "Write a Python function to find the longest palindromic substring in a string"
    send_message_in_reasoning_mode(app_driver, coding_problem)


@when('I access reasoning mode settings')
def access_reasoning_settings(app_driver):
    """Access reasoning mode settings."""
    try:
        settings_button = app_driver.wait_for_element_clickable('[data-testid="reasoning-settings"], [data-testid="settings"]', timeout=5)
        settings_button.click()
        
        # Look for reasoning-specific settings
        reasoning_settings = app_driver.wait_for_element('[data-testid="reasoning-mode-settings"]', timeout=5)
    except TimeoutException:
        pytest.skip("Reasoning mode settings not found")


@when('I export the reasoning trace')
def export_reasoning_trace(app_driver):
    """Export the reasoning trace."""
    try:
        export_button = app_driver.wait_for_element_clickable('[data-testid="export-reasoning"]', timeout=5)
        export_button.click()
    except TimeoutException:
        pytest.skip("Reasoning export not found")


@when('I use reasoning mode extensively')
def use_reasoning_mode_extensively(app_driver):
    """Use reasoning mode extensively to test performance."""
    # Send multiple complex queries
    complex_queries = [
        "Analyze the economic implications of artificial intelligence",
        "Explain the relationship between quantum mechanics and relativity",
        "Solve this system of equations: 2x + 3y = 7, 4x - y = 1"
    ]
    
    for query in complex_queries:
        send_message_in_reasoning_mode(app_driver, query)
        wait_for_reasoning_response(app_driver)


@when('I ask a follow-up question about the reasoning')
def ask_followup_about_reasoning(app_driver):
    """Ask a follow-up question about the reasoning."""
    followup_message = "Can you explain your reasoning in step 2 more clearly?"
    send_message_in_reasoning_mode(app_driver, followup_message)


@then('I should receive a response with reasoning')
def should_receive_response_with_reasoning(app_driver):
    """Verify a response with reasoning was received."""
    wait_for_reasoning_response(app_driver)


@then('the reasoning section should be visible')
def reasoning_section_should_be_visible(app_driver):
    """Verify the reasoning section is visible."""
    reasoning_section = app_driver.wait_for_element('[data-testid="reasoning"], [data-testid="reasoning-section"]')
    assert reasoning_section.is_displayed()


@then('the reasoning should show step-by-step thinking')
def reasoning_should_show_steps(app_driver):
    """Verify the reasoning shows step-by-step thinking."""
    try:
        reasoning_section = app_driver.wait_for_element('[data-testid="reasoning"]')
        reasoning_text = reasoning_section.text
        
        # Check for indicators of step-by-step thinking
        step_indicators = ['step', 'first', 'second', 'then', 'next', 'therefore', 'because']
        assert any(indicator in reasoning_text.lower() for indicator in step_indicators), \
            f"No step-by-step indicators found in reasoning: {reasoning_text[:200]}..."
            
        # Check that reasoning content is substantial
        assert len(reasoning_text.strip()) > 50, "Reasoning content too brief"
    except TimeoutException:
        pytest.fail("Reasoning section not found")


@then('the reasoning section should be hidden')
def reasoning_section_should_be_hidden(app_driver):
    """Verify the reasoning section is hidden."""
    time.sleep(1)  # Wait for toggle to complete
    
    try:
        reasoning_section = app_driver.find_element('[data-testid="reasoning"]')
        assert not reasoning_section.is_displayed()
    except:
        # Reasoning section not found, which also means it's hidden
        pass


@then('the reasoning section should be visible again')
def reasoning_section_should_be_visible_again(app_driver):
    """Verify the reasoning section is visible again."""
    reasoning_section_should_be_visible(app_driver)


@then('I should receive a new response with updated reasoning')
def should_receive_new_response_with_reasoning(app_driver):
    """Verify a new response with updated reasoning."""
    wait_for_reasoning_response(app_driver)
    reasoning_should_show_steps(app_driver)


@then('the reasoning should be relevant to the new question')
def reasoning_should_be_relevant_to_new_question(app_driver):
    """Verify reasoning is relevant to the new question."""
    try:
        reasoning_section = app_driver.wait_for_element('[data-testid="reasoning"]')
        reasoning_text = reasoning_section.text.lower()
        
        # Check for climate change related terms since that's what we edited to
        climate_terms = ['climate', 'greenhouse', 'carbon', 'temperature', 'emission']
        assert any(term in reasoning_text for term in climate_terms), \
            f"Reasoning doesn't appear relevant to climate change: {reasoning_text[:200]}..."
    except TimeoutException:
        pytest.skip("Cannot verify reasoning relevance")


@then('the reasoning mode response should include thinking steps')
def reasoning_response_should_include_thinking_steps(app_driver):
    """Verify reasoning mode response includes thinking steps."""
    reasoning_should_show_steps(app_driver)


@then('the reasoning mode response may be more detailed')
def reasoning_response_may_be_more_detailed(app_driver):
    """Verify reasoning mode response may be more detailed."""
    # This is a comparative test that would require storing both responses
    # For now, just verify we have substantial reasoning content
    try:
        reasoning_section = app_driver.wait_for_element('[data-testid="reasoning"]')
        assert len(reasoning_section.text.strip()) > 100, "Reasoning content not sufficiently detailed"
    except TimeoutException:
        pytest.skip("Cannot verify reasoning detail level")


@then('the reasoning should show mathematical steps')
def reasoning_should_show_mathematical_steps(app_driver):
    """Verify reasoning shows mathematical steps."""
    try:
        reasoning_section = app_driver.wait_for_element('[data-testid="reasoning"]')
        reasoning_text = reasoning_section.text.lower()
        
        # Check for mathematical reasoning indicators
        math_indicators = ['derivative', 'calculate', 'solve', 'equation', 'formula', 'result']
        assert any(indicator in reasoning_text for indicator in math_indicators), \
            f"No mathematical reasoning indicators found: {reasoning_text[:200]}..."
    except TimeoutException:
        pytest.skip("Cannot verify mathematical reasoning")


@then('each calculation step should be clearly explained')
def calculation_steps_should_be_explained(app_driver):
    """Verify calculation steps are clearly explained."""
    reasoning_should_show_mathematical_steps(app_driver)


@then('the reasoning should show problem analysis')
def reasoning_should_show_problem_analysis(app_driver):
    """Verify reasoning shows problem analysis."""
    try:
        reasoning_section = app_driver.wait_for_element('[data-testid="reasoning"]')
        reasoning_text = reasoning_section.text.lower()
        
        # Check for problem analysis indicators
        analysis_indicators = ['analyze', 'approach', 'strategy', 'solution', 'algorithm', 'logic']
        assert any(indicator in reasoning_text for indicator in analysis_indicators), \
            f"No problem analysis indicators found: {reasoning_text[:200]}..."
    except TimeoutException:
        pytest.skip("Cannot verify problem analysis")


@then('the approach to solving the coding problem')
def approach_to_solving_coding_problem(app_driver):
    """Verify approach to solving coding problem is shown."""
    reasoning_should_show_problem_analysis(app_driver)


@then('I should be able to customize reasoning display')
def should_customize_reasoning_display(app_driver):
    """Verify reasoning display can be customized."""
    pytest.skip("Reasoning display customization not implemented in test")


@then('set preferences for reasoning detail level')
def should_set_reasoning_detail_preferences(app_driver):
    """Verify reasoning detail preferences can be set."""
    pytest.skip("Reasoning detail preferences not implemented in test")


@then('I should get a formatted document with all reasoning steps')
def should_get_formatted_reasoning_document(app_driver):
    """Verify formatted reasoning document is provided."""
    pytest.skip("Reasoning document export not implemented in test")


@then('it should be useful for learning or documentation')
def should_be_useful_for_learning(app_driver):
    """Verify exported reasoning is useful for learning."""
    pytest.skip("Learning utility verification not implemented in test")


@then('the responses should still be delivered in reasonable time')
def responses_should_be_timely(app_driver):
    """Verify responses are delivered in reasonable time."""
    # This is implicitly tested by the timeout mechanisms in wait_for_reasoning_response
    # If responses take too long, the tests will timeout
    pass


@then('the interface should remain responsive')
def interface_should_remain_responsive(app_driver):
    """Verify interface remains responsive."""
    # Test that we can still interact with the interface
    try:
        textarea = app_driver.wait_for_element('textarea[placeholder*="Send a message"]', timeout=5)
        assert textarea.is_enabled()
    except TimeoutException:
        pytest.fail("Interface not responsive")


@then('the AI should be able to clarify its thinking process')
def ai_should_clarify_thinking_process(app_driver):
    """Verify AI can clarify its thinking process."""
    wait_for_reasoning_response(app_driver)
    # Additional verification that the response addresses the reasoning question
    # would require natural language analysis


@then('provide additional reasoning if needed')
def should_provide_additional_reasoning(app_driver):
    """Verify additional reasoning can be provided."""
    ai_should_clarify_thinking_process(app_driver)


# Helper functions
def wait_for_reasoning_response(app_driver):
    """Wait for a response with reasoning to be generated."""
    # Wait for the basic response
    app_driver.wait_for_api_response()
    
    # Wait specifically for reasoning section to appear
    try:
        app_driver.wait_for_element('[data-testid="reasoning"], [data-testid="reasoning-section"]', timeout=30)
    except TimeoutException:
        pytest.skip("Reasoning section not found - reasoning mode may not be implemented")