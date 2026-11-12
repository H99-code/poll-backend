
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Poll API")

# Umfrage-Daten
poll = {
    "id": 1,
    "question": "Wie hat euch die Vorlesung gefallen?",
    "options": [
        {"id": 1, "text": "Sehr gut"},
        {"id": 2, "text": "Gut"},
        {"id": 3, "text": "Mittelmäßig"},
        {"id": 4, "text": "Schlecht"}
    ]
}

# Ergebnisse
votes = {1: 0, 2: 0, 3: 0, 4: 0}


class VoteRequest(BaseModel):
    poll_id: int
    option_id: int


class PollOption(BaseModel):
    id: int
    text: str


class PollUpdate(BaseModel):
    question: str
    options: list[PollOption]


@app.get("/")
def home():
    return {"message": "Poll API is running!"}


@app.get("/poll")
def get_poll():
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll


@app.post("/vote")
def submit_vote(vote: VoteRequest):
    if poll is None or vote.poll_id != poll["id"]:
        raise HTTPException(status_code=404, detail="Poll not found")

    if vote.option_id not in votes:
        raise HTTPException(status_code=400, detail="Invalid option")

    votes[vote.option_id] += 1

    return {"message": "Vote submitted successfully"}


@app.get("/results")
def get_results():
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")

    return {
        "poll_id": poll["id"],
        "results": [
            {
                "option_id": option["id"],
                "text": option["text"],
                "votes": votes[option["id"]]
            }
            for option in poll["options"]
        ]
    }


@app.put("/poll")
def update_poll(updated_poll: PollUpdate):
    global poll, votes

    poll = {
        "id": 1,
        "question": updated_poll.question,
        "options": [option.model_dump() for option in updated_poll.options]
    }

    votes = {option["id"]: 0 for option in poll["options"]}

    return {"message": "Poll updated successfully", "poll": poll}


@app.delete("/poll")
def delete_poll():
    global poll, votes

    poll = None
    votes = {}

    return {"message": "Poll deleted successfully"}
