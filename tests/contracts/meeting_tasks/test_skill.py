"""Contract of the skill text. It does not show that a model follows it and is no acceptance test."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / 'skills/meeting-tasks/SKILL.md'


class SkillContractTests(unittest.TestCase):
    def test_the_only_skill_loads_the_language_gate_and_is_implemented(self):
        self.assertEqual([SKILL], list((ROOT / 'skills').glob('*/SKILL.md')))
        text = SKILL.read_text(encoding='utf-8')
        self.assertIn('\nname: meeting-tasks\n', text)
        self.assertIn('../_shared/references/operator-language.md', text)
        self.assertNotIn('plugin-skeleton', text)

    def test_the_scripts_it_calls_exist(self):
        text = SKILL.read_text(encoding='utf-8')
        for name in ('read_notes.py', 'save_tasks.py', 'unknown_failure.py'):
            self.assertIn('scripts/' + name, text)
            self.assertTrue((SKILL.parent / 'scripts' / name).is_file())


if __name__ == '__main__':
    unittest.main()
