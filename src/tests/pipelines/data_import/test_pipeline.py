from unittest import TestCase

import pandas as pd
from phantasyfootballer.common import PLAYER_NAME
from phantasyfootballer.pipelines.data_import.nodes import (
    _replace_player_name,
    fixup_player_names,
)


class TestNodes(TestCase):
    def test_replace_player_name(self):
        assert _replace_player_name("Gardner Minshew II") == "Gardner Minshew"
        assert _replace_player_name("Michael D") == "Michael D"

    def test_fixup_player_name(self):
        test_frame = pd.DataFrame(
            {
                PLAYER_NAME: [
                    "Gardner Minshew II",
                    "Michael D",
                    "Benny Still Jr.",
                    "Michael Pittman Jr.",
                ]
            }
        )
        expected_frame = pd.DataFrame(
            {
                PLAYER_NAME: [
                    "Gardner Minshew",
                    "Michael D",
                    "Benny Still",
                    "Michael Pittman",
                ]
            }
        )
        result = fixup_player_names(test_frame)
        assert expected_frame.equals(result)
