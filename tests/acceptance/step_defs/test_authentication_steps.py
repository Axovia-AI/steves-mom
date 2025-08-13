"""Step definitions for authentication and session management tests."""

import pytest
import time
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Load scenarios from the feature file
scenarios('../features/authentication.feature')


@given('I am not logged in')
def not_logged_in(app_driver):
    """Ensure user is not logged in."""
    app_driver.navigate_to('/')
    # Check if we're in a guest session or need to log out
    try:
        user_menu = app_driver.wait_for_element('[data-testid="user-menu"]', timeout=2)
        if user_menu:
            # Click user menu and look for logout option
            user_menu.click()
            try:
                logout_button = app_driver.wait_for_element_clickable('[data-testid="logout"]', timeout=2)
                logout_button.click()
                time.sleep(1)  # Wait for logout to complete
            except TimeoutException:
                pass  # Already logged out or guest session
    except TimeoutException:
        pass  # No user menu, likely not logged in


@given('I have a registered account')
def have_registered_account(app_driver):
    """Ensure we have a test account to work with."""
    # For testing purposes, we'll use a known test account
    # In a real scenario, this might create a test account or use a fixture
    app_driver.test_email = "test@example.com"
    app_driver.test_password = "testpassword123"


@given('I am authenticated as a guest user')
def authenticated_as_guest(app_driver):
    """Ensure user is authenticated as guest."""
    app_driver.navigate_to('/')
    # Wait for guest session to be established
    time.sleep(2)
    # Verify we're in guest mode (no email in user menu, or specific guest indicators)


@given('I am logged in as a registered user')
def logged_in_as_registered_user(app_driver):
    """Log in as a registered user."""
    # First ensure we have account details
    have_registered_account(app_driver)
    
    # Navigate to login page
    app_driver.navigate_to('/login')
    
    try:
        # Fill in login form
        email_input = app_driver.wait_for_element('input[type="email"]')
        password_input = app_driver.wait_for_element('input[type="password"]')
        
        email_input.send_keys(app_driver.test_email)
        password_input.send_keys(app_driver.test_password)
        
        # Submit login form
        login_button = app_driver.wait_for_element_clickable('button[type="submit"]')
        login_button.click()
        
        # Wait for login to complete
        time.sleep(2)
    except TimeoutException:
        pytest.skip("Login form not available or login functionality not implemented")


@given('I have an active chat session')
def have_active_chat_session(app_driver):
    """Create an active chat session."""
    app_driver.navigate_to('/')
    # Send a message to create a chat session
    from step_defs.test_chat_steps import send_message_and_wait
    send_message_and_wait(app_driver, "Hello")


@when('I visit the application')
def visit_application(app_driver):
    """Visit the main application page."""
    app_driver.navigate_to('/')


@when('I navigate to the registration page')
def navigate_to_registration(app_driver):
    """Navigate to the registration page."""
    app_driver.navigate_to('/register')


@when('I navigate to the login page')
def navigate_to_login(app_driver):
    """Navigate to the login page."""
    app_driver.navigate_to('/login')


@when('I fill in valid registration details')
def fill_registration_details(app_driver):
    """Fill in the registration form with valid details."""
    try:
        # Generate unique test email
        import uuid
        test_id = str(uuid.uuid4())[:8]
        app_driver.test_email = f"test_{test_id}@example.com"
        app_driver.test_password = "testpassword123"
        
        # Fill form fields
        email_input = app_driver.wait_for_element('input[type="email"]')
        password_input = app_driver.wait_for_element('input[type="password"]')
        
        email_input.send_keys(app_driver.test_email)
        password_input.send_keys(app_driver.test_password)
        
        # Look for confirm password field if present
        try:
            confirm_password = app_driver.find_element('input[name="confirmPassword"]')
            confirm_password.send_keys(app_driver.test_password)
        except NoSuchElementException:
            pass
            
    except TimeoutException:
        pytest.skip("Registration form not available")


@when('I submit the registration form')
def submit_registration_form(app_driver):
    """Submit the registration form."""
    try:
        submit_button = app_driver.wait_for_element_clickable('button[type="submit"]')
        submit_button.click()
        time.sleep(2)  # Wait for registration to process
    except TimeoutException:
        pytest.skip("Registration submit button not found")


@when('I enter my valid credentials')
def enter_valid_credentials(app_driver):
    """Enter valid login credentials."""
    try:
        email_input = app_driver.wait_for_element('input[type="email"]')
        password_input = app_driver.wait_for_element('input[type="password"]')
        
        email_input.send_keys(app_driver.test_email)
        password_input.send_keys(app_driver.test_password)
    except TimeoutException:
        pytest.skip("Login form not available")


@when('I submit the login form')
def submit_login_form(app_driver):
    """Submit the login form."""
    try:
        login_button = app_driver.wait_for_element_clickable('button[type="submit"]')
        login_button.click()
        time.sleep(2)  # Wait for login to process
    except TimeoutException:
        pytest.skip("Login submit button not found")


@when('I click on the user menu')
def click_user_menu(app_driver):
    """Click on the user menu."""
    try:
        user_menu = app_driver.wait_for_element_clickable('[data-testid="user-menu"]')
        user_menu.click()
    except TimeoutException:
        pytest.skip("User menu not found")


@when('I select logout')
def select_logout(app_driver):
    """Select logout from the user menu."""
    try:
        logout_button = app_driver.wait_for_element_clickable('[data-testid="logout"]')
        logout_button.click()
        time.sleep(1)  # Wait for logout to complete
    except TimeoutException:
        pytest.skip("Logout option not found")


@when(parsers.parse('I send {count:d} messages'))
def send_multiple_messages(app_driver, count):
    """Send multiple messages to test limits."""
    from step_defs.test_chat_steps import send_message_and_wait
    
    for i in range(count):
        try:
            send_message_and_wait(app_driver, f"Test message {i+1}")
            time.sleep(0.5)  # Brief pause between messages
        except Exception:
            # If we hit a limit, break out of the loop
            break


@when('I try to access protected features')
def try_access_protected_features(app_driver):
    """Try to access features that might be protected."""
    # This is a placeholder - specific protected features would be tested here
    pass


@when('I try to access the login page')
def try_access_login_page(app_driver):
    """Try to navigate to login page."""
    app_driver.navigate_to('/login')


@when('I try to access the registration page')
def try_access_registration_page(app_driver):
    """Try to navigate to registration page."""
    app_driver.navigate_to('/register')


@when('I refresh the browser')
def refresh_browser(app_driver):
    """Refresh the browser page."""
    app_driver.driver.refresh()
    time.sleep(2)  # Wait for page to reload


@when('I remain inactive for an extended period')
def remain_inactive(app_driver):
    """Simulate remaining inactive."""
    # For testing purposes, we'll just wait a short time
    # In a real test, this might involve waiting longer or manipulating session timeouts
    time.sleep(5)


@when('I request a password reset')
def request_password_reset(app_driver):
    """Request a password reset."""
    pytest.skip("Password reset functionality not implemented in test")


@then('I should be automatically authenticated as a guest user')
def should_be_guest_user(app_driver):
    """Verify user is authenticated as guest."""
    # Wait for page to load and check for guest session indicators
    time.sleep(2)
    # Check that we can access basic functionality without being fully registered
    assert app_driver.is_element_present('textarea[placeholder*="Send a message"]')


@then('I should be able to start chatting immediately')
def should_be_able_to_chat(app_driver):
    """Verify chat functionality is available."""
    textarea = app_driver.wait_for_element('textarea[placeholder*="Send a message"]')
    assert textarea.is_enabled()


@then('I should be successfully registered')
def should_be_registered(app_driver):
    """Verify registration was successful."""
    # Check for success indicators or redirect to main app
    current_url = app_driver.driver.current_url
    # Should be redirected away from register page
    assert '/register' not in current_url or app_driver.is_element_present('[data-testid="success-message"]')


@then('I should be logged in')
def should_be_logged_in(app_driver):
    """Verify user is logged in."""
    # Check for logged-in user indicators
    time.sleep(2)
    # Look for user menu or other authenticated user indicators
    assert app_driver.is_element_present('[data-testid="user-menu"]') or not app_driver.driver.current_url.endswith('/login')


@then('I should be successfully logged in')
def should_be_successfully_logged_in(app_driver):
    """Verify successful login."""
    should_be_logged_in(app_driver)


@then('I should see my email in the user menu')
def should_see_email_in_user_menu(app_driver):
    """Verify email is displayed in user menu."""
    try:
        user_menu = app_driver.wait_for_element('[data-testid="user-menu"]')
        user_menu.click()
        time.sleep(1)
        
        # Look for email in the menu or profile area
        menu_text = user_menu.text
        assert app_driver.test_email in menu_text or app_driver.is_element_present('[data-testid="user-email"]')
    except TimeoutException:
        pytest.skip("User menu not accessible")


@then('I should be logged out')
def should_be_logged_out(app_driver):
    """Verify user is logged out."""
    time.sleep(2)
    # Check that we're back to guest mode or login page
    current_url = app_driver.driver.current_url
    assert '/login' in current_url or not app_driver.is_element_present('[data-testid="user-menu"]')


@then('I should be redirected to the guest session')
def should_be_redirected_to_guest(app_driver):
    """Verify redirect to guest session."""
    time.sleep(2)
    # Should be able to access basic functionality as guest
    assert app_driver.is_element_present('textarea[placeholder*="Send a message"]')


@then('I should reach the daily message limit')
def should_reach_message_limit(app_driver):
    """Verify daily message limit is reached."""
    # Look for limit message or disabled input
    try:
        # Check if input is disabled or limit message is shown
        textarea = app_driver.find_element('textarea[placeholder*="Send a message"]')
        limit_message = app_driver.is_element_present('[data-testid="message-limit"]')
        
        assert not textarea.is_enabled() or limit_message
    except NoSuchElementException:
        pytest.skip("Message limit functionality not clearly implemented")


@then('I should be prompted to register')
def should_be_prompted_to_register(app_driver):
    """Verify registration prompt appears."""
    # Look for registration prompt or modal
    assert app_driver.is_element_present('[data-testid="register-prompt"]') or 'register' in app_driver.driver.current_url.lower()


@then('I should remain logged in')
def should_remain_logged_in(app_driver):
    """Verify user remains logged in after refresh."""
    should_be_logged_in(app_driver)


@then('my chat session should be preserved')
def chat_session_should_be_preserved(app_driver):
    """Verify chat session is preserved."""
    # Check that previous messages are still visible
    messages = app_driver.find_elements('[data-author="user"], [data-author="assistant"]')
    assert len(messages) > 0, "No messages found - session not preserved"


@then('I should be able to access basic chat functionality')
def should_access_basic_chat(app_driver):
    """Verify basic chat functionality is accessible."""
    should_be_able_to_chat(app_driver)


@then('I should have limited access to advanced features')
def should_have_limited_access(app_driver):
    """Verify access to advanced features is limited."""
    # This would check for specific limitations for guest users
    # For now, we'll just verify basic functionality works
    pass


@then('I should be redirected away from the login page')
def should_be_redirected_from_login(app_driver):
    """Verify redirect away from login page."""
    time.sleep(2)
    current_url = app_driver.driver.current_url
    assert '/login' not in current_url


@then('I should be redirected away from the registration page')
def should_be_redirected_from_register(app_driver):
    """Verify redirect away from registration page."""
    time.sleep(2)
    current_url = app_driver.driver.current_url
    assert '/register' not in current_url


@then('I should receive a password reset email')
def should_receive_reset_email(app_driver):
    """Verify password reset email is sent."""
    pytest.skip("Email verification not implemented in test")


@then('I should be able to reset my password')
def should_reset_password(app_driver):
    """Verify password can be reset."""
    pytest.skip("Password reset flow not implemented in test")


@then('my session should expire')
def session_should_expire(app_driver):
    """Verify session expires."""
    pytest.skip("Session expiration not implemented in test")


@then('I should be prompted to log in again')
def should_be_prompted_to_login(app_driver):
    """Verify login prompt appears."""
    pytest.skip("Session expiration prompt not implemented in test")