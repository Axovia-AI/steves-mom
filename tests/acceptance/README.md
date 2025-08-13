# Acceptance Tests

This directory contains behavior-driven development (BDD) acceptance tests using pytest-bdd for the AI chatbot application.

## Overview

The acceptance tests are written in Gherkin syntax and cover the main features of the application:

- **Chat Functionality** - Core messaging and AI response features
- **Authentication & Session Management** - User login, registration, and session handling
- **Artifacts Management** - Creation and management of structured content
- **Document Management** - Document creation, editing, and sharing
- **Message Voting System** - User feedback on AI responses
- **Reasoning Mode** - AI reasoning and step-by-step explanations

## Structure

```
tests/acceptance/
├── features/           # Gherkin feature files
│   ├── chat.feature
│   ├── authentication.feature
│   ├── artifacts.feature
│   ├── documents.feature
│   ├── voting.feature
│   └── reasoning.feature
├── step_defs/          # Python step definitions
│   ├── test_chat_steps.py
│   ├── test_authentication_steps.py
│   ├── test_artifacts_steps.py
│   ├── test_documents_steps.py
│   ├── test_voting_steps.py
│   └── test_reasoning_steps.py
├── support/            # Test utilities and helpers
│   └── app_driver.py
└── conftest.py         # pytest configuration
```

## Prerequisites

1. **Python 3.8+** with the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Application Server** running on http://localhost:3000:
   ```bash
   pnpm dev
   ```

3. **Chrome Browser** (for Selenium WebDriver)

## Running Tests

### Quick Start

Run all smoke tests (most important scenarios):
```bash
python run_acceptance_tests.py --markers "smoke"
```

### All Test Categories

```bash
# Run all acceptance tests
python run_acceptance_tests.py

# Run specific feature tests
python run_acceptance_tests.py --pattern "chat"
python run_acceptance_tests.py --pattern "authentication"

# Run only implemented features (exclude skipped scenarios)
python run_acceptance_tests.py --markers "not skip_unimplemented"

# Run with verbose output
python run_acceptance_tests.py --verbose

# Run specific scenario
python run_acceptance_tests.py --pattern "Send a basic message"
```

### Direct pytest Commands

```bash
# Run specific test file
python -m pytest tests/acceptance/step_defs/test_chat_steps.py -v

# Run with specific markers
python -m pytest tests/acceptance/step_defs/ -m "smoke" -v

# Generate test report
python -m pytest tests/acceptance/step_defs/ --html=report.html
```

## Test Markers

- `@smoke` - Critical functionality tests that should always pass
- `@integration` - Tests that involve multiple components
- `@skip_unimplemented` - Features not yet implemented (automatically skipped)

## Environment Configuration

The tests automatically:
- Check if the application server is running before starting
- Use headless Chrome for browser automation
- Wait for application responses with appropriate timeouts
- Handle authentication and session management

## Feature Status

### ✅ Implemented and Tested
- Basic chat messaging
- User authentication (guest and registered users)
- File upload functionality
- Message voting (upvote/downvote)
- Weather tool integration

### 🚧 Partially Implemented
- Artifacts creation and management
- Document management
- Reasoning mode functionality

### ⏳ Planned (Currently Skipped)
- Advanced artifacts features (sharing, versioning)
- Multi-user document collaboration
- Advanced reasoning mode features
- Session persistence and recovery
- Advanced search and filtering

## Writing New Tests

### 1. Add Feature File

Create a new `.feature` file in `tests/acceptance/features/`:

```gherkin
Feature: New Feature
  As a user
  I want to do something
  So that I can achieve a goal

  Scenario: Basic scenario
    Given I am on the application
    When I perform an action
    Then I should see a result
```

### 2. Implement Step Definitions

Create corresponding step definitions in `tests/acceptance/step_defs/`:

```python
from pytest_bdd import scenarios, given, when, then

scenarios('../features/new_feature.feature')

@given('I am on the application')
def on_application(app_driver):
    app_driver.navigate_to('/')

@when('I perform an action')
def perform_action(app_driver):
    # Implementation here
    pass

@then('I should see a result')
def should_see_result(app_driver):
    # Assertions here
    assert True
```

### 3. Mark Unimplemented Features

For features not yet implemented, add the `@skip_unimplemented` marker:

```gherkin
@skip_unimplemented
Scenario: Future feature
  Given something exists
  When I do something new
  Then something should happen
```

## Best Practices

1. **Use descriptive scenario names** that clearly explain the behavior being tested
2. **Keep scenarios focused** on a single piece of functionality
3. **Use Background sections** to reduce duplication in feature files
4. **Mark unimplemented features** with `@skip_unimplemented` rather than deleting them
5. **Write robust selectors** that are unlikely to break with UI changes
6. **Use appropriate timeouts** for async operations
7. **Clean up test data** when necessary to avoid test interference

## Troubleshooting

### Common Issues

**Server not running:**
```
Error: Application server is not running.
Please start it with: pnpm dev
```
Solution: Start the development server with `pnpm dev`

**Chrome driver issues:**
```
WebDriverException: unknown error: cannot find Chrome binary
```
Solution: Install Chrome browser or set CHROME_BIN environment variable

**Element not found:**
```
TimeoutException: Message: element not found
```
Solution: Check if the UI has changed, update selectors, or increase timeouts

**Test hanging:**
```
Test appears to be stuck or taking too long
```
Solution: Check for infinite loading states, increase timeouts, or verify server responses

### Debug Mode

For debugging failing tests:

1. **Remove headless mode** - Edit `app_driver.py` and comment out the `--headless` option
2. **Add breakpoints** - Use `import pdb; pdb.set_trace()` in step definitions
3. **Increase timeouts** - Modify timeout values in `app_driver.py`
4. **Check browser console** - Use `app_driver.driver.get_log('browser')` to see browser errors

## Contributing

When adding new acceptance tests:

1. Follow the existing patterns in feature files and step definitions
2. Ensure tests are deterministic and can run in any order
3. Add appropriate markers (`@smoke`, `@skip_unimplemented`, etc.)
4. Update this README if adding new features or changing test structure
5. Test your changes against a running application instance