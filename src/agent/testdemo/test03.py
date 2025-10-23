from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:2024")

for chunk in client.runs.stream(
        None,  # Threadless run
        "agent",  # Name of assistant. Defined in langgraph.json.
        input={
            "messages": [{
                "role": "human",
                "content": "我是顾翔",
            }],
        },
        stream_mode="messages-tuple",
):
    print(f"Receiving new event of type: {chunk.event}...")
    print(chunk.data)
    print("\n\n")

    # print(chunk.data)
    # if isinstance(chunk.data, list) and 'type' in chunk.data[0] and chunk.data[0]['type'] == 'AIMessageChunk':
    #     print(chunk.data[0]['content'], end='|')
