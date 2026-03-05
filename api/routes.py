from fastapi import APIRouter
from analyzer import analyze
from api.schemas import ExplainRequest
from service.explain_function import explain_function
# Dev1 miner import (adjust if function name differs)
from miner.git_processor import mine_git_history
from .webhook import webhook_router
from db.repository import update_function, get_existing_analysis


router = APIRouter()

@router.post("/analyze")
def analyze_function(repo_path: str, filepath: str, function_name: str):

    # Step 1 — Mine Git history
    git_context = mine_git_history(
        repo_path,
        filepath,
        function_name
    )

    # Step 2 — Run analyzer
    analysis, ownership = analyze(git_context)

    # Step 3 — Store in MongoDB
    data = {
        "repo": git_context.repo,
        "filepath": git_context.filepath,
        "function_name": git_context.function_name,

        "analysis": {
            "callers": analysis.callers,
            "callees": analysis.callees,
            "blast_radius": analysis.blast_radius
        },

        "ownership": {
            "primary_owner": ownership.primary_owner,
            "confidence": ownership.confidence
        }
    }

    update_function(
        git_context.repo,
        git_context.filepath,
        git_context.function_name,
        data
    )

    return {
        "analysis": analysis,
        "ownership": ownership
    }




@router.post("/explain-function")
def explain(req: ExplainRequest):

    # check Mongo cache first
    existing = get_existing_analysis(
        req.repo_name,
        req.filepath,
        req.function_name
    )

    if existing and "decision_log" in existing:
        print('existing')
        return existing["decision_log"]

    # compute explanation
    result = explain_function(
        repo_path=req.repo_path,
        filepath=req.filepath,
        function_name=req.function_name,
        owner=req.owner,
        repo_name=req.repo_name
    )

    # store in Mongo
    update_function(
        req.repo_name,
        req.filepath,
        req.function_name,
        {
            "decision_log": {
                "why_it_exists": result.why_it_exists,
                "key_decisions": result.key_decisions,
                "linked_issues": result.linked_issues,
                "generated_at": result.generated_at
            }
        }
    )

    return result


# include webhook routes
router.include_router(webhook_router)