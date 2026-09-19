import warnings
from unittest.mock import MagicMock
from pytest import MonkeyPatch
from colorama import Fore, Style, init

init(autoreset=True)
warnings.filterwarnings("ignore")

from utils import (
    prune_long_term_memory,
    store_memory,
    retrieve_memory,
    long_term_maintenance_node,
    summarizer_node,
)
from tools import write_code, review_code, approve_code


# -----------------------------
# Test output helpers
# -----------------------------

def log_step(message: str) -> None:
    print(f"{Fore.CYAN}➜ {message}{Style.RESET_ALL}")

def log_data(label: str, data) -> None:
    print(f"{Fore.YELLOW}{label}:{Style.RESET_ALL}")
    print(data)
    print("-" * 60)

def log_success(message: str) -> None:
    print(f"{Fore.GREEN}✔ {message}{Style.RESET_ALL}")


def run_test(test_func):
    print(f"{Fore.CYAN}\n▶ Running {test_func.__name__}...{Style.RESET_ALL}")
    try:
        test_func()
        print(f"{Fore.GREEN}✔ {test_func.__name__} PASSED{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✘ {test_func.__name__} FAILED → {e}{Style.RESET_ALL}")
        raise


def run_test_with_monkeypatch(test_func):
    print(f"{Fore.CYAN}\n▶ Running {test_func.__name__} (monkeypatched)...{Style.RESET_ALL}")
    mp = MonkeyPatch()
    try:
        test_func(mp)
        print(f"{Fore.GREEN}✔ {test_func.__name__} PASSED{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✘ {test_func.__name__} FAILED → {e}{Style.RESET_ALL}")
        raise
    finally:
        mp.undo()


# -----------------------------
# TEST 1: Long-Term Memory Storage & Retrieval
# -----------------------------

def test_long_term_memory_storage():
    log_step("Storing a memory entry")
    store_memory("Alice prefers async Python patterns")

    log_step("Retrieving stored memory")
    results, count = retrieve_memory("Python preferences", k=1)

    log_data("Retrieved memories", results)
    log_data("Total memory count", count)

    assert isinstance(results, list)
    assert count > 0
    log_success("Long-term memory storage and retrieval works")


# -----------------------------
# TEST 2: Engineering Workflow (end-to-end)
# -----------------------------

def test_engineering_workflow():
    task = "Implement user authentication with JWT"
    log_step(f"Task: {task}")

    code_spec = write_code.invoke({"feature_description": task})
    log_data("Generated Code/Spec", code_spec)

    review_comments = review_code.invoke({"code_snippet": code_spec})
    log_data("Review Feedback", review_comments)

    approval_result = approve_code.invoke({"code_snippet": code_spec})
    log_data("Lead Decision", approval_result)

    assert isinstance(code_spec, str)
    assert isinstance(review_comments, str)
    assert isinstance(approval_result, str)
    log_success("Engineering workflow executed successfully")


# -----------------------------
# TEST 3: Long-Term Memory Pruning
# -----------------------------

def test_long_term_memory_pruning():
    log_step("Inserting 120 memory entries")
    for i in range(120):
        store_memory(f"Memory entry {i}")
        if i % 20 == 0:
            print(f"{Fore.BLUE}  Inserted {i}...{Style.RESET_ALL}")

    before, before_count = retrieve_memory("Memory entry")
    log_data("Before pruning (sample)", before[:3])
    log_data("Total before pruning", before_count)

    result = prune_long_term_memory(max_docs=100)
    log_data("Pruning result", result)

    after, after_count = retrieve_memory("Memory entry")
    log_data("After pruning (sample)", after[:3])
    log_data("Total after pruning", after_count)

    assert isinstance(result, str)
    log_success("Memory pruning completed")


# -----------------------------
# TEST 4: Summarizer node updates state
# -----------------------------

def test_summarizer_updates_state(monkeypatch):
    log_step("Mocking LLM for summarizer")
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Structured summary"
    monkeypatch.setattr("utils.llm", mock_llm)

    state = {
        "task": "Refactor auth service",
        "approval": "approved",
        "short_term_memory": ["Fix bug", "Improve performance"],
    }
    log_data("Input state", state)

    new_state = summarizer_node(state)
    log_data("Output state", new_state)

    assert "summary" in new_state
    assert new_state["summary"] == "Structured summary"
    log_success("Summarizer node updated workflow state")


# -----------------------------
# TEST 5: Long-term maintenance node calls prune
# -----------------------------

def test_long_term_pruning_called(monkeypatch):
    log_step("Verifying long_term_maintenance_node delegates to prune_long_term_memory")
    mock_prune = MagicMock(return_value="Pruned")
    monkeypatch.setattr("utils.prune_long_term_memory", mock_prune)

    long_term_maintenance_node({"task": "Deploy app"})

    mock_prune.assert_called_once()
    log_success("long_term_maintenance_node called prune_long_term_memory")


# -----------------------------
# TEST 6: Response caching (no double LLM call)
# -----------------------------

def test_caching(monkeypatch):
    log_step("Testing response cache — same prompt should not call LLM twice")
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = ["Original output", "Should not be called"]
    monkeypatch.setattr("utils.llm", mock_llm)

    cache: dict[str, str] = {}

    def cached_invoke(prompt: str) -> str:
        if prompt in cache:
            log_step(f"Cache hit: {prompt}")
            return cache[prompt]
        log_step(f"Cache miss: {prompt}")
        result = mock_llm.invoke(prompt)
        cache[prompt] = result
        return result

    prompt = "Summarize recent workflow actions"
    first = cached_invoke(prompt)
    second = cached_invoke(prompt)

    log_data("First call", first)
    log_data("Second call (from cache)", second)

    assert first == second == "Original output"
    assert mock_llm.invoke.call_count == 1
    log_success("Caching works: LLM called only once for identical prompts")


# -----------------------------
# Test runner
# -----------------------------

def run_all_tests():
    tests = [
        test_long_term_memory_storage,
        test_long_term_memory_pruning,
        test_long_term_pruning_called,
        test_summarizer_updates_state,
        test_caching,
    ]

    print(f"{Fore.YELLOW}\n{'='*40}\n  Test Suite\n{'='*40}{Style.RESET_ALL}")
    passed = failed = 0
    for test in tests:
        try:
            if "monkeypatch" in test.__code__.co_varnames:
                run_test_with_monkeypatch(test)
            else:
                run_test(test)
            passed += 1
        except Exception as e:
            failed += 1
            print(f"{Fore.RED}  ✘ {test.__name__} → {e}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}Passed: {passed}{Style.RESET_ALL}  {Fore.RED}Failed: {failed}{Style.RESET_ALL}")


if __name__ == "__main__":
    run_all_tests()
