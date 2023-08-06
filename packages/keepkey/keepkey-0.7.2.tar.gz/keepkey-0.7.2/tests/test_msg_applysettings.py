import time
import unittest
import common

from keepkeylib import messages_pb2 as proto

class TestMsgApplysettings(common.KeepKeyTest):

    def test_apply_settings(self):
        self.setup_mnemonic_pin_passphrase()
        self.assertEqual(self.client.features.label, 'test')

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(label='new label')

        self.assertEqual(self.client.features.label, 'new label')

    def test_invalid_language(self):
        self.setup_mnemonic_pin_passphrase()
        self.assertEqual(self.client.features.language, 'english')

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(language='nonexistent')

        self.assertEqual(self.client.features.language, 'english')

    def test_apply_settings_passphrase(self):
        self.setup_mnemonic_pin_nopassphrase()

        self.assertEqual(self.client.features.passphrase_protection, False)

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=True)

        self.assertEqual(self.client.features.passphrase_protection, True)

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=False)

        self.assertEqual(self.client.features.passphrase_protection, False)

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=True)

        self.assertEqual(self.client.features.passphrase_protection, True)

if __name__ == '__main__':
    unittest.main()
