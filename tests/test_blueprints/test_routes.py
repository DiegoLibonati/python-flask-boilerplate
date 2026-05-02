import pytest


@pytest.mark.unit
class TestRegisterRoutes:
    def test_notes_prefix_is_registered(self, app) -> None:
        rules: list[str] = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/api/v1/notes" in rule for rule in rules)

    def test_note_blueprint_is_registered(self, app) -> None:
        assert "note" in app.blueprints
