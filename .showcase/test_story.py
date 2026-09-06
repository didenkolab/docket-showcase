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

    def test_sprint_events_refuse_missing_retros(self):
        with self.assertRaises(ValueError) as cm:
            story.sprint_events()
        self.assertEqual(str(cm.exception), "Sprint 1 has no retrospective")

    def test_sprint_events_shape_when_retros_present(self):
        saved = [(s.goal, s.retro) for s in story.SPRINTS]
        try:
            for s in story.SPRINTS:
                s.goal = "Goal of " + s.name
                s.retro = "What happened in " + s.name
            evs = story.sprint_events()
            starts = [e for e in evs if e.args["path"] == "docs/sprints/Sprint 1.md"]
            self.assertEqual([e.when for e in starts],
                             [story.at("2026-06-15", 9), story.at("2026-06-26", 17)])
            self.assertIn("## Retrospective", starts[1].args["body"])
            self.assertIn("Goal of Sprint 1", starts[1].args["body"])
            six = [e for e in evs if e.args["path"] == "docs/sprints/Sprint 6.md"]
            self.assertEqual(len(six), 1)                      # running: start only
            seven = [e for e in evs if e.args["path"] == "docs/sprints/Sprint 7.md"]
            self.assertEqual([e.when for e in seven], [story.at("2026-09-04", 16)])
            self.assertNotIn("Retrospective", seven[0].args["body"])
            self.assertEqual(len(evs), 6 + 5 + 1)
        finally:
            for s, (g, r) in zip(story.SPRINTS, saved):
                s.goal, s.retro = g, r

    def test_titles_with_braces_survive_the_message(self):
        ev = story.new(story.at("2026-06-16"), story.PEOPLE["ingrid"], "x", "Render {berth} as a card", "HARBOR")
        self.assertEqual(ev.message.format_map({"x": "HARBOR-1"}), "HARBOR-1: Render {berth} as a card")

if __name__ == "__main__":
    unittest.main()
