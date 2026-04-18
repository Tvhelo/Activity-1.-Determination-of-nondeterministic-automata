import unittest

from automata import determinize, e_closure, e_determinize, sample_enfa, sample_nfa


class AutomataTests(unittest.TestCase):
    def test_determinize_generates_expected_states_and_transitions(self) -> None:
        dfa_states, dfa_alphabet, dfa_transitions, dfa_initial_state, dfa_final_states = determinize(
            sample_nfa()
        )

        self.assertEqual(len(dfa_states), 8)
        self.assertEqual(dfa_alphabet, {"0", "1"})
        self.assertEqual(dfa_initial_state, frozenset({"q0"}))

        self.assertEqual(
            dfa_transitions[(frozenset({"q0"}), "0")],
            frozenset({"q0", "q1"}),
        )
        self.assertEqual(
            dfa_transitions[(frozenset({"q0", "q1"}), "1")],
            frozenset({"q0", "q2"}),
        )
        self.assertIn(frozenset({"q2"}), dfa_final_states)
        self.assertIn(frozenset({"q0", "q2"}), dfa_final_states)
        self.assertNotIn(frozenset({"q0", "q1"}), dfa_final_states)

    def test_e_closure_includes_all_reachable_epsilon_states(self) -> None:
        self.assertEqual(e_closure(sample_enfa(), {"s0"}), {"s0", "s1", "s3"})
        self.assertEqual(e_closure(sample_enfa(), {"s2"}), {"s2"})

    def test_e_determinize_builds_only_reachable_subsets(self) -> None:
        dfa_states, dfa_alphabet, dfa_transitions, dfa_initial_state, dfa_final_states = e_determinize(
            sample_enfa()
        )

        expected_states = {
            frozenset({"s0", "s1", "s3"}),
            frozenset({"s2"}),
            frozenset({"s4"}),
            frozenset(),
        }

        self.assertEqual(dfa_states, expected_states)
        self.assertEqual(dfa_alphabet, {"a", "b"})
        self.assertEqual(dfa_initial_state, frozenset({"s0", "s1", "s3"}))

        self.assertEqual(
            dfa_transitions[(frozenset({"s0", "s1", "s3"}), "a")],
            frozenset({"s2"}),
        )
        self.assertEqual(
            dfa_transitions[(frozenset({"s0", "s1", "s3"}), "b")],
            frozenset({"s4"}),
        )
        self.assertEqual(dfa_transitions[(frozenset({"s2"}), "b")], frozenset({"s2"}))
        self.assertEqual(dfa_transitions[(frozenset({"s4"}), "a")], frozenset({"s4"}))
        self.assertEqual(dfa_transitions[(frozenset(), "a")], frozenset())
        self.assertEqual(dfa_transitions[(frozenset(), "b")], frozenset())

        self.assertEqual(dfa_final_states, {frozenset({"s2"}), frozenset({"s4"})})


if __name__ == "__main__":
    unittest.main()
