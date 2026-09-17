import uuid

from fastapi import APIRouter

from app.agent.graph import agent
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):

    thread_id = request.thread_id or str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config=config,
    )

    last_message = response["messages"][-1]

    return ChatResponse(
        answer=last_message.content,
        thread_id=thread_id,
    )