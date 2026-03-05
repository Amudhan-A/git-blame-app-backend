from miner.git_processor import mine_git_history
from analyzer.analyze import analyze
from llm.prompts import build_decision_log_prompt
from llm.synthesizer import synthesize


def explain_function(repo_path, filepath, function_name, owner, repo_name):

    git_context = mine_git_history(
        repo_path,
        filepath,
        function_name,
        owner,
        repo_name
    )

    analysis, ownership = analyze(git_context)

    prompt = build_decision_log_prompt(
        git_context,
        analysis,
        ownership
    )

    decision_log = synthesize(prompt)

    return decision_log