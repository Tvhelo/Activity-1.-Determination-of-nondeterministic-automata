from __future__ import annotations

from itertools import chain, combinations
from typing import Collection, Dict, FrozenSet, Iterable, Set, Tuple

EPSILON = "ε"

State = str
Symbol = str
SubsetState = FrozenSet[State]
Transitions = Dict[Tuple[State, Symbol], Set[State]]
Automaton = Tuple[Set[State], Set[Symbol], Transitions, State, Set[State]]
DFATransitions = Dict[Tuple[SubsetState, Symbol], SubsetState]
DFA = Tuple[Set[SubsetState], Set[Symbol], DFATransitions, SubsetState, Set[SubsetState]]


def sample_nfa() -> Automaton:
    states = {"q0", "q1", "q2"}
    alphabet = {"0", "1"}
    transitions: Transitions = {
        ("q0", "0"): {"q0", "q1"},
        ("q0", "1"): {"q0"},
        ("q1", "1"): {"q2"},
        ("q2", "0"): {"q2"},
        ("q2", "1"): {"q2"},
    }
    initial_state = "q0"
    final_states = {"q2"}
    return states, alphabet, transitions, initial_state, final_states


def sample_enfa() -> Automaton:
    states = {"s0", "s1", "s2", "s3", "s4"}
    alphabet = {"a", "b"}
    transitions: Transitions = {
        ("s0", EPSILON): {"s1", "s3"},
        ("s1", "a"): {"s2"},
        ("s2", "b"): {"s2"},
        ("s3", "b"): {"s4"},
        ("s4", "a"): {"s4"},
    }
    initial_state = "s0"
    final_states = {"s2", "s4"}
    return states, alphabet, transitions, initial_state, final_states


def powerset(states: Collection[State]) -> Set[SubsetState]:
    ordered_states = sorted(set(states))
    all_subsets = chain.from_iterable(
        combinations(ordered_states, size) for size in range(len(ordered_states) + 1)
    )
    return {frozenset(subset) for subset in all_subsets}


def determinize(automaton: Automaton) -> DFA:
    states, alphabet, transitions, initial_state, final_states = automaton

    dfa_states = powerset(states)
    dfa_transitions: DFATransitions = {}

    for subset in dfa_states:
        for symbol in alphabet:
            reached: Set[State] = set()
            for state in subset:
                reached.update(transitions.get((state, symbol), set()))
            dfa_transitions[(subset, symbol)] = frozenset(reached)

    dfa_initial_state = frozenset({initial_state})
    dfa_final_states = {subset for subset in dfa_states if subset & final_states}

    return dfa_states, set(alphabet), dfa_transitions, dfa_initial_state, dfa_final_states


def e_closure(automaton: Automaton, states: Iterable[State]) -> Set[State]:
    _, _, transitions, _, _ = automaton

    closure = set(states)
    stack = list(closure)

    while stack:
        current = stack.pop()
        for nxt in transitions.get((current, EPSILON), set()):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)

    return closure


def e_determinize(automaton: Automaton) -> DFA:
    _, alphabet, transitions, initial_state, final_states = automaton

    dfa_alphabet = {symbol for symbol in alphabet if symbol != EPSILON}
    dfa_initial_state = frozenset(e_closure(automaton, {initial_state}))

    open_states = [dfa_initial_state]
    visited_states: Set[SubsetState] = {dfa_initial_state}
    dfa_transitions: DFATransitions = {}

    while open_states:
        current_subset = open_states.pop()

        for symbol in dfa_alphabet:
            move_set: Set[State] = set()
            for state in current_subset:
                move_set.update(transitions.get((state, symbol), set()))

            target_subset = frozenset(e_closure(automaton, move_set))
            dfa_transitions[(current_subset, symbol)] = target_subset

            if target_subset not in visited_states:
                visited_states.add(target_subset)
                open_states.append(target_subset)

    dfa_final_states = {subset for subset in visited_states if subset & final_states}

    return visited_states, dfa_alphabet, dfa_transitions, dfa_initial_state, dfa_final_states
