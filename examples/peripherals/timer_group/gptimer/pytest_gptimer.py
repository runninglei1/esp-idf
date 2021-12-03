# SPDX-FileCopyrightText: 2021-2022 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: CC0-1.0

import pytest
from pytest_embedded.dut import Dut


@pytest.mark.supported_targets
@pytest.mark.generic
def test_gptimer_example(dut: Dut) -> None:
    dut.expect(r'Create timer handle', timeout=5)
    dut.expect(r'Start timer, stop it at alarm event', timeout=5)
    res = dut.expect(r'Timer stopped, count=(\d+)', timeout=30)
    stopped_count = res.group(1).decode('utf8')
    assert (1000000 - 10) < int(stopped_count) < (1000000 + 10)

    dut.expect(r'Set count value')
    dut.expect(r'Get count value')
    res = dut.expect(r'Timer count value=(\d+)', timeout=5)
    count_val = res.group(1).decode('utf8')
    assert int(count_val) == 100

    dut.expect(r'Start timer, auto-reload at alarm event', timeout=5)
    res = dut.expect(r'Timer reloaded, count=(\d+)', timeout=5)
    reloaded_count = res.group(1).decode('utf8')
    assert 0 <= int(reloaded_count) < 10

    dut.expect(r'Stop timer')
    dut.expect(r'Update alarm value dynamically')
    for i in range(1,5):
        res = dut.expect(r'Timer alarmed, count=(\d+)', timeout=5)
        alarm_count = res.group(1).decode('utf8')
        assert (i * 1000000 - 10) < int(alarm_count) < (i * 1000000 + 10)

    dut.expect(r'Stop timer')
    dut.expect(r'Delete timer')
