"""Test the NZBGet switches."""
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)

from . import init_integration


async def test_download_switch(hass, nzbget_api) -> None:
    """Test the creation and values of the download switch."""
    instance = nzbget_api.return_value

    entry = await init_integration(hass)
    assert entry

    registry = await hass.helpers.entity_registry.async_get_registry()
    entity_id = "switch.nzbgettest_download"
    entity_entry = registry.async_get(entity_id)
    assert entity_entry
    assert entity_entry.unique_id == f"{entry.entry_id}_download"

    state = hass.states.get(entity_id)
    assert state
    assert state.state == STATE_ON

    # test download paused
    instance.status.return_value["DownloadPaused"] = True

    await hass.helpers.entity_component.async_update_entity(entity_id)
    await hass.async_block_till_done()

    state = hass.states.get(entity_id)
    assert state
    assert state.state == STATE_OFF


async def test_download_switch_services(hass, nzbget_api) -> None:
    """Test download switch services."""
    instance = nzbget_api.return_value

    entry = await init_integration(hass)
    entity_id = "switch.nzbgettest_download"
    assert entry

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_OFF,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )
    instance.pausedownload.assert_called_once()

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )
    instance.resumedownload.assert_called_once()
