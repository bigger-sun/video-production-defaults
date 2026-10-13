import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = (
    ROOT
    / "templates"
    / "01-信息型短视频"
    / "six-card-list"
    / "render.py"
)


def load_template():
    spec = importlib.util.spec_from_file_location("six_card_list_template", TEMPLATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SixCardListTemplateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = load_template()

    def test_default_timing_is_four_second_hook_plus_three_seconds_per_card(self):
        self.assertEqual(self.template.HOOK_DUR, 4.0)
        self.assertEqual(self.template.CARD_DUR, 3.0)
        self.assertEqual(self.template.BGM_VOLUME, 0.48)
        self.assertEqual(
            self.template.DURATION,
            self.template.HOOK_DUR + len(self.template.ITEMS) * 3.0,
        )

    def test_structured_schema_contains_dense_card_fields(self):
        card = self.template.normalize_item(self.template.ITEMS[0])
        self.assertTrue(card["question"])
        self.assertTrue(card["conclusion"])
        self.assertGreaterEqual(len(card["bullets"]), 3)
        self.assertTrue(card["takeaway"])

    def test_legacy_tuple_remains_supported(self):
        card = self.template.normalize_item(("标题", "标签", "结论", "解释"))
        self.assertEqual(card["question"], "标题")
        self.assertEqual(card["conclusion"], ["结论"])
        self.assertEqual(card["bullets"], [["解释"]])
        self.assertEqual(card["takeaway"], [])

    def test_manual_question_lines_must_preserve_exact_text(self):
        card = self.template.normalize_item(
            {
                "question": "DeepSeek Harness是什么？",
                "question_lines": ["DeepSeek Harness", "是什么？"],
                "conclusion": ["结论"],
            }
        )
        self.assertEqual("".join(card["question_lines"]), card["question"])
        with self.assertRaises(AssertionError):
            self.template.normalize_item(
                {
                    "question": "DeepSeek Harness是什么？",
                    "question_lines": ["DeepSeek", "Harness是什么？"],
                    "conclusion": ["结论"],
                }
            )

    def test_representative_frames_render(self):
        hook = self.template.make_frame(3.6)
        first_card = self.template.make_frame(5.5)
        last_card = self.template.make_frame(self.template.DURATION - 0.2)
        self.assertEqual(hook.size, (1080, 1920))
        self.assertEqual(first_card.size, (1080, 1920))
        self.assertEqual(last_card.size, (1080, 1920))


if __name__ == "__main__":
    unittest.main()
