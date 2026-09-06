import datetime as dt, unittest
import story

class StoryTests(unittest.TestCase):
    def test_six_people_with_domain(self):
        self.assertEqual(len(story.PEOPLE), 6)
        self.assertTrue(all(p.email.endswith("@northlight.example") for p in story.PEOPLE.values()))

    def test_sprints_cover_the_twelve_weeks(self):
        self.assertEqual(story.SPRINTS[0].starts, dt.date(2026, 6, 15))
        self.assertEqual(story.SPRINTS[-1].ends, dt.date(2026, 9, 4))
        self.assertEqual(len(story.SPRINTS), 6)
        for a, b in zip(story.SPRINTS, story.SPRINTS[1:]):
            self.assertLess(a.ends, b.starts)

    def test_at(self):
        self.assertEqual(story.at("2026-06-15", 9, 30), dt.datetime(2026, 6, 15, 9, 30))

    def test_move_event_message(self):
        ev = story.move(story.at("2026-06-16"), story.PEOPLE["ingrid"], "x", "Ready")
        self.assertEqual(ev.kind, "set")
        self.assertEqual(ev.args, {"task": "x", "status": "Ready"})
        self.assertEqual(ev.message, "{x}: → Ready")

    def test_labels_are_eight_pages(self):
        evs = story.label_events()
        self.assertEqual(len(evs), 8)
        self.assertTrue(all(e.args["path"].startswith("docs/labels/") for e in evs))

if __name__ == "__main__":
    unittest.main()
