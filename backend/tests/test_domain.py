import pytest
from pydantic import ValidationError

from app.domain.models import InboundMessage


def test_inbound_message_accepts_bounded_supported_input() -> None:
    message = InboundMessage(
        event_id="synthetic-event-1",
        customer_label="Demo visitor",
        text="What are your weekend hours?",
        locale="en",
    )
    assert message.locale == "en"


@pytest.mark.parametrize("locale", ["de", "", "en-US"])
def test_inbound_message_rejects_unsupported_locale(locale: str) -> None:
    with pytest.raises(ValidationError):
        InboundMessage(
            event_id="synthetic-event-1",
            customer_label="Demo visitor",
            text="Hello",
            locale=locale,
        )


def test_inbound_message_rejects_oversized_text() -> None:
    with pytest.raises(ValidationError):
        InboundMessage(
            event_id="synthetic-event-1",
            customer_label="Demo visitor",
            text="x" * 1001,
            locale="en",
        )
