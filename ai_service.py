import json
import subprocess
from fastapi.concurrency import run_in_threadpool

from .data_service import load_initiative_data, VENDOR_FOLDER


async def generate_rfp_text_placeholder(initiative_id: int) -> str:
    """
    Generates placeholder RFP text.
    In a real scenario, this would call the AI model.
    """
    # This is where you would build a prompt and call Ollama
    # For now, it returns a placeholder.
    return f"# RFP for Initiative {initiative_id}\n\nThis is a placeholder RFP."


async def find_vendors_from_ai(initiative_id: int, schema_name: str) -> str:
    """
    Uses Ollama to find vendors based on initiative data.
    """
    initiative_data = await run_in_threadpool(load_initiative_data, initiative_id, schema_name)

    prompt = f"""
You are a pharmaceutical industry sourcing specialist. Based on the following project details, please identify and list 7 potential vendors that would be a good fit.

For each vendor, provide a brief (1-2 sentence) justification for why they are a good match based on the project requirements.

Project Details:
{json.dumps(initiative_data, indent=2)}

Please format your response as a list.
"""

    proc = await run_in_threadpool(
        subprocess.run,
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        text=True,
        check=True
    )
    return proc.stdout.strip()


async def compare_vendors_from_ai(initiative_id: int) -> str:
    """
    Compares vendor responses using Ollama AI.
    """
    combined_path = VENDOR_FOLDER / f"initiative_{initiative_id}" / "combined_vendor_responses.json"
    if not combined_path.exists():
        raise FileNotFoundError("No vendor responses uploaded yet.")

    with open(combined_path) as f:
        vendor_data = json.load(f)

    prompt = f"""
You are an RFP evaluation specialist. Compare the following vendor responses for initiative {initiative_id}.
Each vendor's response includes their proposal for the same RFP.

For each vendor, provide:
1. Summary of key proposal points
2. Evaluation scores (0–10) for each specified criterion.
3. Overall Strengths & Weaknesses
4. Risk or alignment with requirements

Finally, rank all vendors from best to worst, and recommend the top 2–3 for negotiation.

Vendor Responses:
{json.dumps(vendor_data, indent=2)}
"""

    proc = await run_in_threadpool(
        subprocess.run,
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        text=True,
        check=True
    )
    return proc.stdout.strip()