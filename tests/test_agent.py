import asyncio
from app.agent.graph import agent


async def main():
    question = "How many repositories do I have, and which ones are written in Python?"
    print(f"User: {question}\n")

    # [FIX]: config ke andar thread_id pass kiya
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": "test_session"}},
    )

    final_message = response["messages"][-1]
    print(f"RepoPilot Agent:\n{final_message.content}")


if __name__ == "__main__":
    asyncio.run(main())